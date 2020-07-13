# from config import db, app
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath('../'))
from application import db

class UsersInfo(db.Model):
    __tablename__ = 'users_info'
    id = db.Column(db.Integer, primary_key = True)
    user_login = db.Column(db.String(64), index = True, unique = True)
    user_password = db.Column(db.String(120), index = True)
    email = db.Column(db.String(120),index = True, unique = True )

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

class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)
    description = db.Column(db.String(120), index = True)
    typeid = db.Column(db.Integer, db.ForeignKey('type.id'), index = True)
    #!
    type_model = db.relationship("Type", backref=db.backref("Type", uselist=False))
    createdBy = db.Column(db.String(64), index = True)
    createdOn = db.Column(db.String(64), index = True)
    modifiedBy = db.Column(db.String(64), default = "None", index = True)
    modifiedOn = db.Column(db.String(64), default = "None", index = True)

    def update(self, name, description, typeid, modifiedBy, modifiedOn):
        self.name = name
        self.description = description
        self.typeid = typeid
        self.modifiedBy = modifiedBy
        self.modifiedOn = modifiedOn
        return self 

    def __repr__(self):
        return "<Machine {}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n>".format(self.id, self.name,self.description,self.typeid,self.createdOn,
        self.createdBy,self.modifiedOn,self.modifiedBy,self.type_model)
    
    def __eq__(self, other):
        if isinstance(other, Machine):
            if self.id == other.id and \
                self.name == other.name  and \
                self.description == other.description and \
                self.typeid == other.typeid:
                    return True
        return NotImplemented        

class Type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.String(64), index = True)

