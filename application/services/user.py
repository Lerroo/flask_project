import os
import sys
import logging
import bcrypt
import uuid


from flask import session

print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
# from utils import ValidationException
 
from ..models import MachineArchive, UsersInfo
from ..db_app import db
from .utils import ValidationException


def check_password(password, hash_password):
    if hash_password:
        if bcrypt.checkpw(password.encode(), hash_password):
            return True
    return False

def token_create(): 
    return str(uuid.uuid4().hex)

def email_and_password_valid(dict_v):
    email = dict_v['email']
    password = dict_v['password']
    u = UsersInfo
    query_email_and_password = db.session.query(u.user_login, u.email, u.user_password) \
        .filter(u.email == email) \
        .first()
    if query_email_and_password is not None:
        if check_password(password, query_email_and_password[2]):
            session['name_usr'] = query_email_and_password[0]
            logging.info("User {} log in".format(session.get('name_usr')))
            session.modified = True
            return True
        else:
            raise (ValidationException('password'))
    raise (ValidationException('log_err'))


def password_enc(dict_v):
    dict_v['password'] = bcrypt.hashpw(dict_v.get('password').encode(), bcrypt.gensalt())
    return dict_v
