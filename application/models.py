
import os
import sys
from flask import Flask, request, redirect, url_for, abort, render_template, session

import logging
from sqlalchemy import exc

sys.path.append(os.path.abspath('../'))
from application import db
from main_functions import now_time_iso

class UsersInfo(db.Model):
    __tablename__ = 'users_info'
    id = db.Column(db.Integer, primary_key = True)
    user_login = db.Column(db.String(64), index = True, unique = True)
    user_password = db.Column(db.String(120), index = True)
    email = db.Column(db.String(120),index = True, unique = True )

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except exc.IntegrityError as err:
            s = str(err)
            # message должно лежать поле которое error
            db.session.rollback()
            return render_template('sign_up.html', message='unique err')
        

    def __init__(self, email, login, password):
        self.user_login = login
        self.user_password = password
        self.email = email


    def __repr__(self):
        return "<UsersInfo {}\n{}\n{}\n{}>".format(self.id, self.user_login,self.user_password,
        self.email)

class MachineArchive(db.Model):
    __tablename__ = 'machine_archive'
    id = db.Column(db.Integer, primary_key = True)
    machine_id = db.Column(db.Integer, index = True)
    name = db.Column(db.String(64), index = True)
    description = db.Column(db.String(120), index = True)
    type_value = db.Column(db.String(64), index = True)
    createdBy = db.Column(db.String(64), index = True)
    createdOn = db.Column(db.String(64), index = True)
    modifiedBy = db.Column(db.String(64), default = "None", index = True)
    modifiedOn = db.Column(db.String(64), default = "None", index = True)

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
            #time iso
            logging.info("Archive update ({})".format(now_time_iso()[11:]))
        except:
            logging.error("#500. An error has happened add method!({})".format(now_time_iso()[11:]))
            abort(500)
        # return self
        return self

class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)
    description = db.Column(db.String(120), index = True)
    typeid = db.Column(db.Integer, db.ForeignKey('type.id'), index = True)
    type_model = db.relationship("Type", backref=db.backref("Type", uselist=False))
    createdBy = db.Column(db.String(64), index = True)
    createdOn = db.Column(db.String(64), index = True)
    modifiedBy = db.Column(db.String(64), default = "None", index = True)
    modifiedOn = db.Column(db.String(64), default = "None", index = True)

    def __init__(self, name, description, typeid, createdBy=None, createdOn=None, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.typeid = typeid
        self.createdBy = createdBy
        self.createdOn = createdOn
        # logging.info("User {} requested information #{}({})".format(createdBy, id, now_time_iso()[11:]))

    def update(self, name, description, typeid, modifiedBy, modifiedOn):
        self.name = name
        self.description = description
        self.typeid = typeid
        self.modifiedBy = modifiedBy
        self.modifiedOn = modifiedOn
        try:
            #
            db.session.commit()
            logging.info("User {} changed info #{}({})".format(modifiedBy, self.id, now_time_iso()[11:]))
            return self 
        except:
            logging.error("#500. An error has happened!!({})".format(now_time_iso()[11:]))
            abort(500)
        

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            #time iso
            logging.info("{} add new machine at {}({})".format(
                self.createdBy, self.createdOn, now_time_iso()[11:]))
        except:
            #Отделн функц
            logging.error("#500. An error has happened add method!({})".format(now_time_iso()[11:]))
            abort(500)
        # return self
        return self 

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            logging.error("#500. An error has happened delete method!({})".format(now_time_iso()[11:]))
            abort(500) 

    def __repr__(self):
        return "<Machine {}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n>".format(self.id, self.name,self.description,self.typeid,self.createdOn,
        self.createdBy,self.modifiedOn,self.modifiedBy,self.type_model)
    
    def __eq__(self, other):
        if isinstance(other, Machine):
            if self.name == other.name  and \
                self.description == other.description and \
                self.typeid == other.typeid:
                    return True
        return NotImplemented        

class Type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.String(64), index = True)

