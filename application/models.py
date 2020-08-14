import os
import sys
from flask import Flask, request, abort, render_template, session, g

import logging
from sqlalchemy import exc
import json

from .db_app import app, db


class UsersInfo(db.Model):
    __tablename__ = 'users_info'
    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(64), unique=True)
    user_password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    token = db.Column(db.String(120), unique=True)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            logging.info("Add new user {} ".format(self.user_login))
        except exc.IntegrityError as err:
            db.session.rollback()
            logging.error("#500. An error IntegrityError")
            return render_template('sign_up.html', message='unique err')
        except exc.OperationalError as err:
            logging.error("#500. An error OperationalError(database locked)")
            abort(500)

    @staticmethod
    def verify_auth_token(token):
        user_id = db.session.query(UsersInfo.id, UsersInfo.user_login) \
            .filter(UsersInfo.token == token) \
            .first()
        return user_id

    def __init__(self, user, password, email, token):
        self.user_login = user
        self.user_password = password
        self.email = email
        self.token = token

    def __repr__(self):
        return "<UsersInfo {}\n{}\n{}\n{}>".format(self.id, self.user_login, self.user_password,
                                                   self.email)


class MachineArchive(db.Model):
    __tablename__ = 'machine_archive'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(120))
    type_value = db.Column(db.String(64))
    createdBy = db.Column(db.String(64))
    createdOn = db.Column(db.String(64))
    modifiedBy = db.Column(db.String(64), default="None")
    modifiedOn = db.Column(db.String(64), default="None")

    def __init__(self, machine):
        self.machine_id = machine.id
        self.name = machine.name
        self.description = machine.description
        self.type_value = machine.type_model.value
        self.createdBy = machine.createdBy
        self.createdOn = machine.createdOn
        self.modifiedBy = machine.modifiedBy
        self.modifiedOn = machine.modifiedOn

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            logging.info("Archive {} add machine".format(self.id))
        except exc.OperationalError as err:
            logging.error("#500. An error OperationalError(database locked)")
            abort(500)
        except:
            logging.error("#500. Server error!")
            abort(500)
        return self


class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(120))
    typeid = db.Column(db.Integer, db.ForeignKey('type.id'), index=True)
    type_model = db.relationship("Type", backref=db.backref("Type", uselist=False))
    createdBy = db.Column(db.String(64))
    createdOn = db.Column(db.String(64))
    modifiedBy = db.Column(db.String(64), default="None")
    modifiedOn = db.Column(db.String(64), default="None")

    def __init__(self, name, description, select_type, createdBy=None, createdOn=None, id=None, modifiedBy=None,
                 modifiedOn=None):
        self.id = id
        self.name = name
        self.description = description
        self.typeid = int(select_type)
        self.createdBy = createdBy
        self.createdOn = createdOn
        self.modifiedBy = modifiedBy
        self.modifiedOn = modifiedOn

    def update(self, new_machine):
        self.name = new_machine.name
        self.description = new_machine.description
        self.typeid = new_machine.typeid
        self.modifiedBy = new_machine.modifiedBy
        self.modifiedOn = new_machine.modifiedOn
        try:
            db.session.commit()
            logging.info("User {} changed info #{}".format(self.modifiedBy, self.id))
        except exc.OperationalError as err:
            logging.error("#500. An error OperationalError(database locked)")
            abort(500)
        except:
            logging.error("#500. Server error!")
            abort(500)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            logging.info("{} add new machine at {}".format(
                self.createdBy, self.createdOn))
        except exc.OperationalError as err:
            logging.error("#500. An error OperationalError(database locked)")
            abort(500)
        except:
            logging.error("#500. Server error!")
            abort(500)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            logging.warning("{} delete {} machine".format(session['name_usr'], self.id))
        except exc.OperationalError as err:
            logging.error("#500. An error OperationalError(database locked)")
            abort(500)
        except:
            logging.error("#500. Server error!")
            abort(500)


    @property
    def dict(self):
        return {'id':self.id,
            'name':self.name, 
            'description':self.description, 
            'typeid':self.typeid, 
            'createdBy':self.createdBy, 
            'createdOn':self.createdOn, 
            'modifiedBy':self.modifiedBy, 
            'modifiedOn':self.modifiedOn}

    def __repr__(self):
        return "<Machine {}\nname {}\n desc {}\n typeid {}\n{}\n{}\n{}\n{}\n{}\n>".format(self.id, self.name,
                                                                                          self.description,
                                                                                          self.typeid,
                                                                                          self.createdOn,
                                                                                          self.createdBy,
                                                                                          self.modifiedOn,
                                                                                          self.modifiedBy,
                                                                                          self.type_model)

    def __eq__(self, other):
        if isinstance(other, Machine):
            if self.name == other.name and \
                    self.description == other.description and \
                    self.typeid == other.typeid:
                return True
        return NotImplemented


class Type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(64), unique=True)

    def __init__(self, value):
        self.value = value

    def add(self):
        try
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError as err:
            db.session.rollback()
            logging.error("An error IntegrityError an Type().add")


class MachineMetric(db.Model):
    __tablename__ = 'machine_metric'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users_info.id'), index=True)
    data = db.Column(db.String(64))
    time_stamp = db.Column(db.String(64))

    def __init__(self, machine_id, data, user_id, time_stamp):
        self.machine_id = machine_id
        self.user_id = user_id
        self.data = json.dumps(json.loads(data), indent=4, sort_keys=True)
        self.time_stamp = time_stamp

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            logging.info("#{} add new metric {}".format(self.user_id, self.id))
        except exc.OperationalError as err:
            logging.error("#500. An error OperationalError(database locked)")
            abort(500)
        except:
            logging.error("#500. Server error!")
            abort(500)