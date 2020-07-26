from flask import Flask, jsonify, request, abort, g, session
import os
import sys
import curl
from flask_httpauth import HTTPBasicAuth 

auth = HTTPBasicAuth()

sys.path.append(os.path.abspath('../../'))
from application import db, app
from application.services.utils import now_time_iso, json_validate
from application.models import Machine, Type, MachineArchive, MachineMetric, UsersInfo

#logging models
#auth.login_required
#json err

#remove-item alias:\curl

#curl -i -u 1646875ea2344fbb809adbcb32570b04:unused -H "Content-Type: application/json" -X POST -d '{"""name""":"""name""", """description""":"""description""", """select_type""":1}' http://localhost:5000/api/machine
@app.route('/api/machine', methods=['POST'])
@auth.login_required
def api_new_machine():
    """add"""
    json_d = json_validate(request.json, 3)
    if json_d:
        new_v = {
            'createdBy':session['name_usr'],
            'createdOn':now_time_iso()
        }
        json_d.update(new_v)
        Machine(**json_d).add()
    else:
        json_d = {
            'error':'error json'
        }
        abort(401)
    return jsonify(machine=json_d), 201

# curl -i http://127.0.0.1:5000/api/machines
@app.route('/api/machines', methods=['GET'])
def api_get_machines():
    """show all"""
    machines = Machine.query.all()
    return jsonify(machines=[machine.dict for machine in machines])

#curl -i http://127.0.0.1:5000/api/machine/54
@app.route('/api/machine/<int:machine_id>', methods=['GET'])
def api_get_machine(machine_id):
    """show id"""
    return jsonify(machine=Machine.query.get_or_404(machine_id).dict)

#curl -i -u 1646875ea2344fbb809adbcb32570b04:unused -H "Content-Type: application/json" -X PUT -d '{"""name""":"""name""", """description""":"""description""", """select_type""":"""1"""}' http://localhost:5000/api/machine/40
@app.route('/api/machine/<int:machine_id>', methods=['PUT'])
@auth.login_required
def api_update_machine(machine_id):
    """update id"""
    json_d = json_validate(request.json, 3)
    if json_d and Machine.query.get(machine_id):
        json_d.update({'modifiedBy':session['name_usr'], 'modifiedOn':now_time_iso()})
        new_m = Machine(**json_d)
        old_m = Machine.query.get_or_404(machine_id)
        old_m.update(new_m)
    else:
        json_d = {
            'error':'error json or machine_id'
        }
        abort(401)
    return jsonify(machine=old_m.dict)

#curl -i -u 1646875ea2344fbb809adbcb32570b04:unused -H "Content-Type: application/json" -X DELETE http://localhost:5000/api/machine/40
@app.route('/api/machine/<int:machine_id>', methods=['DELETE'])
@auth.login_required
def api_delete_machine(machine_id):
    """delete id"""
    if Machine.query.get(machine_id):
        m = Machine.query.get_or_404(machine_id)
        m.delete()
        json_d = m.dict
    else:
        json_d = {
            'error':'error machine_id'
        }
        abort(401)
    return jsonify(machine=json_d)


@auth.verify_password
def verify_password(token, password):
    user = UsersInfo.verify_auth_token(token)
    if not user:
        return False
    session['name_usr'] = user.user_login
    session['user_id'] = user.id
    return True

#curl -i -u 1646875ea2344fbb809adbcb32570b04:unused -H "Content-Type: application/json" -X POST -d '{"""metrics""":"""metrics"""}' http://localhost:5000/api/machine/40/metric
@app.route('/api/machine/<int:machine_id>/metric', methods=['POST'])
@auth.login_required
def api_new_metric(machine_id):
    json_d = json_validate(request.json, 1)
    if json_d and Machine.query.get(machine_id):
        new_v = {
            'machine_id':machine_id,
            'user_id':session['user_id'],
            'time_stamp':now_time_iso()
        }
        json_d.update(new_v)
        MachineMetric(**json_d).add()
    else:
        json_d = {
            'error':'error json or machine_id'
        }
        abort(401)
    return jsonify(machine=json_d), 201



