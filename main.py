from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import bcrypt
import json
from datetime import datetime

from models import Users_info, Machines, Type, Machine_archive
from config import db, app

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
        u = Users_info(
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

@app.route('/sign_in/', methods=['post', 'get'])
def login():
    message = ''    
    if request.method == 'POST':    
        email = request.form.get('email') 
        password = str(request.form.get('password'))
        query_email_and_password = db.session.query(Users_info.user_login, Users_info.email, Users_info.user_password) \
            .filter(Users_info.email == email) \
            .first()
        if check_password(password, query_email_and_password[2]):
            session['name_usr'] = query_email_and_password[0]
            log_message("User {} log in".format(session.get('name_usr')))
            session.modified = True
            return redirect("/machines")
        else:
            return redirect("/sign_in")
    if request.method == 'GET':
        message = 'Input email and password'     
    return render_template('sign_in.html', message=message)

@app.route('/machines', methods=['get'])
def machines():
    if request.method == 'GET':
        items = Machines.query.all() 
        return render_template('machines.html', items=items)

@app.route('/machine/new/', methods=['post', 'get'])
def new():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        if not name or not description:
            return redirect("/machines/new")
        typeid = request.form.get('select_type')
        createdBy = session.get('name_usr')
        machines = Machines(
            name=name, 
            description=description, 
            typeid=typeid, 
            createdBy=createdBy,
            createdOn=now_time_iso())
        try:
            db.session.add(machines)
            db.session.commit()
            log_message("{} add new machine at {}".format(createdBy, machines.createdOn))
            return redirect(url_for('machines'))
        except:
            abort(404)
    else:
        type_list = Type.query.all()
        return render_template('machines_new.html', type_list=type_list)

@app.route('/machine/del/<int:id>', methods=['post', 'get'])
def machines_del(id):
    machine = Machines.query.get_or_404(id)
    try:
        db.session.delete(machine)
        db.session.commit()
        return redirect(url_for('machines'))
    except:
        abort(404)     

@app.route('/machine/<int:id>', methods=['post', 'GET'])
def machines_info(id):
    name_usr = session.get('name_usr')
    if request.method == "GET":
        machine = Machines.query.get(id)
        type_list = Type.query.all()
        log_message("User {} requested information #{}".format(name_usr, id))
        return render_template("machines_info.html", machine=machine, type_list=type_list)
    else:
        # POST
        machine = Machines.query.get_or_404(id)
        new_machine = Machines(
            id=id,
            name=request.form['name'], 
            description=request.form['description'], 
            typeid=int(request.form['select_type']), 
        )
        if machine != new_machine:
            archive = Machine_archive(
                machine_id=id,
                name=machine.name,
                description=machine.description,
                type_value=machine.type_model.value,
                createdBy=machine.createdBy,
                createdOn=machine.createdOn,
                modifiedBy=machine.modifiedBy,
                modifiedOn=machine.modifiedOn
            )
            try:
                db.session.add(archive)
                db.session.commit()
                log_message("Archive update")
            except:
                abort(404)
            machine = machine.update(
                new_machine.name,
                new_machine.description,
                new_machine.typeid,
                name_usr,
                now_time_iso())
            try:
                db.session.commit()
            except:
                abort(404)
            log_message("User {} changed info #{}".format(name_usr, id))
            return redirect(url_for('machines'))
        else:
            #!
            print('22222222222222222222222')
            return redirect(url_for('/machines', id=id))

@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
def forbidden(error):
    return render_template('404.html',message=error)


@app.route('/')
def index():
    return render_template('index.html', message='Сhoose your direction.')  

if __name__ == "__main__":
    app.run()