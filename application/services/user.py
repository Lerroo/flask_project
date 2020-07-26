import os
import sys
import logging
import bcrypt
import uuid


from flask import session

sys.path.append(os.path.abspath('../../'))
import application.models as model
from application.services.utils import ValidationException
from application import db


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
    user = model.UsersInfo
    query_email_and_password = db.session.query(user.user_login, user.email, user.user_password) \
        .filter(user.email == email) \
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
