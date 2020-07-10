from flask import Flask, request, redirect, url_for, abort, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import bcrypt
import json
from datetime import datetime
import logging

from models import UsersInfo, Machine, Type, MachineArchive
from config import db,app

def log_message(message):
    print('-'*10 + message + '-'*10)

def now_time_iso():
    return datetime.now().isoformat(sep='T', timespec="seconds")
    
def check_password(password, hash_password):
    if hash_password:
        if bcrypt.checkpw(password.encode(), hash_password):
            return True
    return False

@app.route('/sign_up/', methods=['post', 'get'])
def sign_up():
    message = 'Input your personal data'
    if request.method == 'POST':
        user_g = request.form.get('user') 
        email_g = request.form.get('email')  
        password_g = request.form.get('password')
        if not user_g or not email_g or not password_g:
            return render_template('sign_up.html', message='Incorect email or username')
        u = UsersInfo(
            user_login=user_g,
            email=email_g, 
            user_password=bcrypt.hashpw(password_g.encode(), bcrypt.gensalt())
        )
        db.session.add(u)
        try:
            db.session.commit()
            message = 'Your data is saved'
        except exc.SQLAlchemyError:
            return render_template('sign_up.html', message='Incorect email or username')
    return render_template('sign_up.html', message=message)  

def check_password(password, hash_password):
    if hash_password:
        if bcrypt.checkpw(password.encode(), hash_password):
            return True
    return False

@app.route('/sign_in/', methods=['post', 'get'])
def login():
    message = ''    
    if request.method == 'POST':    
        email = request.form.get('email') 
        password = str(request.form.get('password'))
        query_email_and_password = db.session.query(UsersInfo.user_login, UsersInfo.email, UsersInfo.user_password) \
            .filter(UsersInfo.email == email) \
            .first()
        if check_password(password, query_email_and_password[2]):
            session['name_usr'] = query_email_and_password[0]
            logging.info("User {} log in".format(session.get('name_usr')))
            session.modified = True
            return redirect("/machines")
        else:
            return redirect("/sign_in")
    else:
        message = 'Input email and password'     
    return render_template('sign_in.html', message=message)

@app.route('/machines', methods=['get'])
def machines():
    items = Machine.query.all() 
    return render_template('Machines.html', items=items)

@app.route('/machine/new/', methods=['post', 'get'])
def new():
    if request.method == "POST":
        createdBy = session.get('name_usr')
        if not createdBy:
            abort(401)
        name = request.form['name']
        description = request.form['description']
        if not name or not description:
            return redirect("/machines/new")
        typeid = request.form.get('select_type')
        machines = Machine(
            name=name, 
            description=description, 
            typeid=typeid, 
            createdBy=createdBy,
            createdOn=now_time_iso())
        try:
            db.session.add(machines)
            db.session.commit()
            logging.info("{} add new machine at {}({})".format(createdBy, Machine.createdOn, now_time_iso()[11:]))
            return redirect(url_for('machines'))
        except:
            pass
    else:
        type_list = Type.query.all()
        return render_template('machines_new.html', type_list=type_list)

@app.route('/machine/del/<int:id>', methods=['post', 'get'])
def machines_del(id):
    machine = Machine.query.get_or_404(id)
    try:
        db.session.delete(machine)
        db.session.commit()
        return redirect(url_for('machines'))
    except:
        logging.error("#500. An error has happened!({})".format(now_time_iso()[11:]))
        abort(500)     

@app.route('/machine/<int:id>', methods=['post', 'GET'])
def machines_info(id):
    name_usr = session.get('name_usr')
    if request.method == "GET":
        machine = Machine.query.get(id)
        type_list = Type.query.all()
        logging.info("User {} requested information #{}({})".format(name_usr, id, now_time_iso()[11:]))
        return render_template("machines_info.html", machine=machine, type_list=type_list)
    else:
        # POST
        machine = Machine.query.get_or_404(id)
        new_machine = Machine(
            id=id,
            name=request.form['name'], 
            description=request.form['description'], 
            typeid=int(request.form['select_type']), 
        )
        if machine != new_machine:
            archive = MachineArchive(machine)
            try:
                db.session.add(archive)
                db.session.commit()
                logging.info("Archive update ({})".format(now_time_iso()[11:]))
            except:
                logging.error("#500. An error has happened!({})".format(now_time_iso()[11:]))
                abort(500)
            machine = machine.update(
                new_machine.name,
                new_machine.description,
                new_machine.typeid,
                name_usr,
                now_time_iso())
            try:
                db.session.commit()
            except:
                logging.error("#500. An error has happened!({})".format(now_time_iso()[11:]))
                abort(500)
            logging.info("User {} changed info #{}({})".format(name_usr, id, now_time_iso()[11:]))
            return redirect(url_for('machines'))
        else:
            return redirect(url_for('/machines'))

@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def forbidden(error):
    return render_template('404.html',message=error)


@app.route('/')
def index():
    return render_template('index.html', message='Сhoose your direction.')  

if __name__ == "__main__":
    logging.basicConfig(filename='log_'+str(now_time_iso()[:-9])+'.log', level=logging.INFO)
    

    app.run()