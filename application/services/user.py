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


def validate_email_and_password(dict_v):
    email = dict_v['email']
    password = dict_v['password']
    u = UsersInfo
    stored_email_password  = db.session.query(u.user_login, u.user_password) \
        .filter(u.email == email) \
        .first()
    if stored_email_password is not None:
        print(stored_email_password)
        if check_password(password, stored_email_password[1]):
            save_user_to_session(stored_email_password[0])
            return True
        else:
            raise (ValidationException('password'))
    raise (ValidationException('log_err'))


def save_user_to_session(user):
    session['name_usr'] = user
    logging.info("User {} log in".format(user))
    session.modified = True

def encrypt_password(passw):
    return bcrypt.hashpw(passw.encode(), bcrypt.gensalt())

def prepare_user(dict_v):
    dict_v['password'] = encrypt_password(dict_v['password'])
    dict_v.update({'token':token_create()})
    return dict_v
