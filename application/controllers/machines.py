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
        machine_value.extend([session.get('name_usr'), now_time_iso()])
        Machine(*machine_value).add()
        return redirect(url_for('machines'))  
    except ValidationException as error:
        type_list = Type.query.all()
        return render_template("machines_new.html", type_list=type_list, message=error)
  

@app.route('/machine/del/<int:id>', methods=['get'])
def machines_del(id):
    machine = Machine.query.get_or_404(id)
    MachineArchive(machine).add()
    machine.delete()
    return redirect(url_for('machines', _external=True))    


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
        int(request.form['select_type']), modifiedBy=session.get('name_usr'),
            modifiedOn=now_time_iso())
    if machine != new_machine:
        MachineArchive(machine).add()
        machine.update(new_machine)    
        return redirect(url_for('machines', _external=True))
    else:
        return redirect(url_for('machines', _external=True))