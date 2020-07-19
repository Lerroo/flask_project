from flask import Flask, request, redirect, url_for, abort, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime
import logging
import os
import sys

sys.path.append(os.path.abspath('../../'))
from application import db, app
from application.models import Machine, Type, MachineArchive
from application.services.utils import type_list, ValidationException, now_time_iso, \
convert_to_dict_values, session_name
from application.services.machine import convert_to_dict_machine


@app.route('/machines', methods=['get'])
def machines():
    if session_name():
        items = Machine.query.all() 
        return render_template('machines.html', items=items)

@app.route('/machine/new/', methods=['get'])
def new_get():
    if session_name():
        return render_template('machines_new.html', type_list=type_list)
    

@app.route('/machine/new/', methods=['post'])
def new():
    try:
        machine_dict = convert_to_dict_values(request.form.to_dict())
        new_v = {'createdBy':str(session.get('name_usr')), 'createdOn':now_time_iso()}
        Machine(**convert_to_dict_machine(machine_dict, new_v)).add()
        return redirect(url_for('machines'))  
    except ValidationException as error:
        return render_template("machines_new.html", type_list=type_list, message=error)
  

@app.route('/machine/del/<int:id>', methods=['get'])
def machines_del(id):
    if session_name():
        machine = Machine.query.get_or_404(id)
        MachineArchive(machine).add()
        machine.delete()
        return redirect(url_for('machines', _external=True))    


@app.route('/machine/<int:id>', methods=['get'])
def machines_info_get(id):
    if session_name():
        machine = Machine.query.get_or_404(id)
        return render_template("machines_info.html", machine=machine, type_list=type_list)


@app.route('/machine/<int:id>', methods=['post'])
def machines_info(id):     
    machine = Machine.query.get_or_404(id)
    new_v = {'modifiedBy':session.get('name_usr'), 'modifiedOn':now_time_iso()}
    new_machine = Machine(**convert_to_dict_machine(request.form.to_dict(), new_v))
    if machine != new_machine:
        MachineArchive(machine).add()
        machine.update(new_machine)    
        return redirect(url_for('machines', _external=True))
    else:
        return redirect(url_for('machines', _external=True))
