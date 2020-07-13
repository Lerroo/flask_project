from flask import Flask, request, redirect, url_for, abort, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime
import logging
import os
import sys

sys.path.append(os.path.abspath('../../'))
from application.models import UsersInfo, Machine, Type, MachineArchive
from application import db, app


def now_time_iso():
    return datetime.now().isoformat(sep='T', timespec="seconds")


@app.route('/machines', methods=['get'])
def machines():
    items = Machine.query.all() 
    return render_template('Machines.html', items=items)


@app.route('/machine/new/', methods=['post', 'get'])
def new():
    type_list = Type.query.all()
    if request.method == "POST":
        createdBy = session.get('name_usr')
        if not createdBy:
            abort(401)
        name = request.form['name']
        description = request.form['description']
        if not name :
            return render_template("machines_new.html",type_list=type_list, message="error name") 
        else:
            if not description:
                return render_template("machines_new.html",type_list=type_list, message="error description") 
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
        machine = Machine.query.get_or_404(id)
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
                logging.error("#500. An error has happened!!({})".format(now_time_iso()[11:]))
                abort(500)
            logging.info("User {} changed info #{}({})".format(name_usr, id, now_time_iso()[11:]))
            return redirect(url_for('machines', _external=True))
        else:
            return redirect(url_for('machines', _external=True))