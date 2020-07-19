import os
import sys
from flask import Flask, request, abort, render_template, session

import logging
from sqlalchemy import exc

sys.path.append(os.path.abspath('../'))
from application import db, app


class UsersInfo(db.Model):
    __tablename__ = 'users_info'
    id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(64), index=True, unique=True)
    user_password = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            logging.info("Add new user {} ".format(self.user_login))
        except exc.IntegrityError as err:
            db.session.rollback()
            logging.error("#500. An error IntegrityError has happened add method!")
            return render_template('sign_up.html', message='unique err')
        except exc.OperationalError as err:
            logging.error("#500. An error OperationalError(database locked) has happened add method!")
            abort(500)

    def __init__(self, user, password, email):
        self.user_login = user
        self.user_password = password
        self.email = email

    def __repr__(self):
        return "<UsersInfo {}\n{}\n{}\n{}>".format(self.id, self.user_login, self.user_password,
                                                   self.email)


class MachineArchive(db.Model):
    __tablename__ = 'machine_archive'
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(120), index=True)
    type_value = db.Column(db.String(64), index=True)
    createdBy = db.Column(db.String(64), index=True)
    createdOn = db.Column(db.String(64), index=True)
    modifiedBy = db.Column(db.String(64), default="None", index=True)
    modifiedOn = db.Column(db.String(64), default="None", index=True)

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
            logging.info("Archive update ")
        except exc.OperationalError as err:
            logging.error("#500. An error OperationalError(database locked) has happened add method!")
            abort(500)
        except:
            logging.error("#500. An error has happened add method!")
            abort(500)
        return self


class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(120), index=True)
    typeid = db.Column(db.Integer, db.ForeignKey('type.id'), index=True)
    type_model = db.relationship("Type", backref=db.backref("Type", uselist=False))
    createdBy = db.Column(db.String(64), index=True)
    createdOn = db.Column(db.String(64), index=True)
    modifiedBy = db.Column(db.String(64), default="None", index=True)
    modifiedOn = db.Column(db.String(64), default="None", index=True)

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
            logging.error("#500. An error OperationalError(database locked) has happened add method!")
            abort(500)
        except:
            logging.error("#500. An error has happened!!")
            abort(500)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            logging.info("{} add new machine at {}".format(
                self.createdBy, self.createdOn))
        except exc.OperationalError as err:
            logging.error("#500. An error OperationalError(database locked) has happened add method!")
            abort(500)
        except:
            logging.error("#500. An error has happened add method!")
            abort(500)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except exc.OperationalError as err:
            logging.error("#500. An error OperationalError(database locked) has happened add method!")
            abort(500)
        except:
            logging.error("#500. An error has happened delete method!{}", 'ho')
            abort(500)

    def __repr__(self):
        return "<Machine {}\nname {}\n desc {}\n typeid {}\n{}\n{}\n{}\n{}\n{}\n>".format(self.id, type(self.name),
                                                                                          type(self.description),
                                                                                          type(self.typeid),
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
    value = db.Column(db.String(64), index=True)
