from flask import Flask, request, redirect, url_for, abort, render_template, session
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import exc, func

from datetime import datetime
import logging
import os
import sys


from ..db_app import db, app
from ..models import Machine, Type, MachineArchive, UsersInfo, MachineMetric
from ..services.utils import type_list, ValidationException, now_time_iso, \
    valudate_values, check_page_accses



@app.route('/machines', methods=['get'])
def machines():
    if check_page_accses():
        user_t = db.session.query(UsersInfo.token) \
            .filter(UsersInfo.user_login == session.get('name_usr')) \
            .first()
        user_inf = {
            'token':user_t[0],
            'name':session.get('name_usr')
        }
        machine_id_counts = db.session.query(MachineMetric.machine_id, func.count('id') \
            .label('count')).group_by(MachineMetric.machine_id).subquery()
        query = db.session.query(Machine, machine_id_counts.c.count) \
            .outerjoin(machine_id_counts, machine_id_counts.c.machine_id == Machine.id) \
            .all()
        return render_template('machines.html', items=query, user_inf=user_inf)
    else: abort(401)

@app.route('/machine/new/', methods=['get'])
def new_get():
    if check_page_accses():
        return render_template('machines_new.html', type_list=type_list)
    else: abort(401)
    

@app.route('/machine/new/', methods=['post'])
def new():
    try:
        machine_dict = request.form.to_dict()
        if valudate_values(machine_dict):
            new_v = {'createdBy':str(session.get('name_usr')), 'createdOn':now_time_iso()}
            machine_dict.update(new_v)
            Machine(**machine_dict).add()
            return redirect(url_for('machines'))  
    except ValidationException as error:
        return render_template("machines_new.html", type_list=type_list, message=error)
  

@app.route('/machine/del/<int:id>', methods=['get'])
def machines_del(id):
    if check_page_accses():
        machine = Machine.query.get_or_404(id)
        MachineArchive(machine).add()
        machine.delete()
        return redirect(url_for('machines', _external=True))    
    else: abort(401)


@app.route('/machine/<int:id>', methods=['get'])
def machines_info_get(id):
    if check_page_accses():
        machine = Machine.query.get_or_404(id)
        return render_template("machines_info.html", machine=machine, type_list=type_list)
    else: abort(401)


@app.route('/machine/<int:id>', methods=['post'])
def machines_info(id):     
    machine = Machine.query.get_or_404(id)
    machine_dict = request.form.to_dict()
    if valudate_values(machine_dict):
        new_v = {'modifiedBy':session.get('name_usr'), 'modifiedOn':now_time_iso()}
        machine_dict.update(new_v)
        new_machine = Machine(**machine_dict)
        if machine != new_machine:
            MachineArchive(machine).add()
            machine.update(new_machine)    
            return redirect(url_for('machines', _external=True))
        else:
            return redirect(url_for('machines', _external=True))


@app.route('/machine/<int:id>/metrics', methods=['get'])
def machines_info_get_metrics(id):
    if check_page_accses():
        metrics = MachineMetric.query.filter(MachineMetric.machine_id == id).all()
        return render_template("metrics.html", metrics=metrics)
    else: abort(401)