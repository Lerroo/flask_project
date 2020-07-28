import os
import sys
import logging
import bcrypt
import uuid


from flask import session

 
from ..models import MachineArchive, UsersInfo
from ..db_app import db
from .utils import ValidationException


def check_password(password, hash_password):
    return hash_password and bcrypt.checkpw(password.encode(), hash_password)

def token_create(): 
    return str(uuid.uuid4().hex)

def email_and_password_valid(dict_v):
    email = dict_v['email']
    password = dict_v['password']
    u = UsersInfo
    stored_email_password  = db.session.query(u.user_login, u.user_password) \
        .filter(u.email == email) \
        .first()
    if stored_email_password  is not None:
        if check_password(password, stored_email_password[2]):
            session['name_usr'] = stored_email_password[0]
            logging.info("User {} log in".format(session.get('name_usr')))
            session.modified = True
            return True
        else:
            raise (ValidationException('password'))
    raise (ValidationException('log_err'))


def prepare_user(dict_v):
    dict_v['password'] = bcrypt.hashpw(dict_v.get('password').encode(), bcrypt.gensalt())
    dict_v.update({'token':token_create()})
    return dict_v
