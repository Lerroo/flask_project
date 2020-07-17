from flask import Flask, render_template, session, abort
from datetime import datetime
import logging
import bcrypt

from application import db, app
import application.models as model

class ValidationException(Exception):
    exception_dict = {
        'name':'error name input',
        'description':'error description input',
        'email':'error email',
        'password':'error password',
        'log_err':'login failed',
        'user':'Incorect username',
        'email':'Incorect email'
    }

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.exception_dict.get(self.name)

def password_enc(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hash_password):
    if hash_password:
        if bcrypt.checkpw(password.encode(), hash_password):
            return True
    return False

def convert_to_list_values(values_form):
    # decorator
    # createdBy = session.get('name_usr')
    # if not createdBy:
    #     abort(401)
    for k, v in values_form.items():
        if v == '':
            raise (ValidationException(k))
    return list(values_form.values())

def email_and_password_valid(email, password):
    #
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
    return False  
        

def now_time_iso():
    return datetime.now().isoformat(sep='T', timespec="seconds")


@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def forbidden(error):
    return render_template('404.html',message=error)

@app.route('/')
def index():
    return render_template('index.html', message='Сhoose your direction.')  