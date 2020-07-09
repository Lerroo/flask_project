from config import db
from datetime import datetime


class Users_info(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_login = db.Column(db.String(64), index = True, unique = True)
    user_password = db.Column(db.String(120), index = True)
    email = db.Column(db.String(120),index = True, unique = True )

class Machine_archive(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    machine_id = db.Column(db.Integer, index = True)
    name = db.Column(db.String(64), index = True)
    description = db.Column(db.String(120), index = True)
    type_value = db.Column(db.String(64), index = True)
    createdBy = db.Column(db.String(64), index = True)
    createdOn = db.Column(db.String(64), index = True)
    modifiedBy = db.Column(db.String(64), default = "None", index = True)
    modifiedOn = db.Column(db.String(64), default = "None", index = True)

class Machines(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)
    description = db.Column(db.String(120), index = True)
    typeid = db.Column(db.Integer, db.ForeignKey('type.id'), index = True)
    type_model = db.relationship("Type", backref=db.backref("type", uselist=False))
    createdBy = db.Column(db.String(64), index = True)
    createdOn = db.Column(db.String(64), index = True)
    modifiedBy = db.Column(db.String(64), default = "None", index = True)
    modifiedOn = db.Column(db.String(64), default = "None", index = True)#, default=datetime.now().isoformat(sep='T', timespec="seconds"))

    def update(self, name, description, typeid, modifiedBy, modifiedOn):
        self.name = name
        self.description = description
        self.typeid = typeid
        self.modifiedBy = modifiedBy
        self.modifiedOn = modifiedOn
        return self 


    def __repr__(self):
        return "<Machines {}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n>".format(self.id, self.name,self.description,self.typeid,self.createdOn,
        self.createdBy,self.modifiedOn,self.modifiedBy,self.type_model)
    
    def __eq__(self, other):
        if isinstance(other, Machines):
            if self.id == other.id and \
                self.name == other.name  and \
                self.description == other.description and \
                self.typeid == other.typeid:
                    return True
        return NotImplemented
        

class Type(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.String(64), index = True)

