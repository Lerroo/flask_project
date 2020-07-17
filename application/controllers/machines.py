from flask import Flask, request, redirect, url_for, abort, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime
import logging
import os
import sys

sys.path.append(os.path.abspath('../../'))
from application.models import Machine, Type, MachineArchive
from application import db, app
from main_functions import now_time_iso, ValidationException, convert_to_list_values




def name_session_check():
    pass


@app.route('/machines', methods=['get'])
def machines():
    items = Machine.query.all() 
    return render_template('machines.html', items=items)

@app.route('/machine/new/', methods=['get'])
def new_get():
    type_list = Type.query.all()#
    return render_template('machines_new.html', type_list=type_list)
    

@app.route('/machine/new/', methods=['post'])
def new():
    try:
        machine_value = convert_to_list_values(request.form)
        machine = machine_value.extend([session.get('name_usr'), now_time_iso()])
        Machine(*machine).add()
        return redirect(url_for('machines'))  
    except ValidationException as error:
        type_list = Type.query.all()
        return render_template("machines_new.html", type_list=type_list, message=error)
  

@app.route('/machine/del/<int:id>', methods=['get'])
def machines_del(id):
    machine = Machine.query.get_or_404(id)
<<<<<<< HEAD
    MachineArchive(machine).add()
    machine.delete()
    return redirect(url_for('machines'))  
=======
    try:
        db.session.add(MachineArchive(machine))
        db.session.commit()
        logging.info("Archive update ({})".format(now_time_iso()[11:]))
    except:
        logging.error("#500. An error has happened!({})".format(now_time_iso()[11:]))
        abort(500)
    try:
        db.session.delete(machine)
        db.session.commit()
        return redirect(url_for('machines'))
    except:
        logging.error("#500. An error has happened!({})".format(now_time_iso()[11:]))
        abort(500)     
>>>>>>> 69e095aaefd848d07eda16313c07d1a4abd9178c


@app.route('/machine/<int:id>', methods=['get'])
def machines_info_get(id):
    machine = Machine.query.get_or_404(id)
    type_list = Type.query.all()
    # models str91
    # name_usr = session.get('name_usr')
    # logging.info("User {} requested information #{}({})".format(name_usr, id, now_time_iso()[11:]))
    return render_template("machines_info.html", machine=machine, type_list=type_list)


@app.route('/machine/<int:id>', methods=['post'])
def machines_info(id):     
    machine = Machine.query.get_or_404(id)
    new_machine = Machine(request.form['name'], request.form['description'], 
        int(request.form['select_type']))
    if machine != new_machine:
        MachineArchive(machine).add()
        machine.update(new_machine.name,
            new_machine.description,
            new_machine.typeid,
            session.get('name_usr'),
            now_time_iso())        
        return redirect(url_for('machines', _external=True))
    else:
        return redirect(url_for('machines', _external=True))