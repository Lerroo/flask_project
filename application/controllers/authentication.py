from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import bcrypt
import os
import sys

from datetime import datetime
import logging

sys.path.append(os.path.abspath('../../'))
from application.models import UsersInfo, Machine, Type, MachineArchive
from application import db, app


def check_password(password, hash_password):
    if hash_password:
        if bcrypt.checkpw(password.encode(), hash_password):
            return True
    return False


@app.route('/sign_up/', methods=['post', 'get'])
def sign_up():
    message = 'Input your personal data'
    if request.method == 'POST':
        user_g = request.form.get('user') 
        email_g = request.form.get('email')  
        password_g = request.form.get('password')
        if not user_g or not email_g or not password_g:
            return render_template('sign_up.html', message='Incorect email or username')
        u = UsersInfo(
            user_login=user_g,
            email=email_g, 
            user_password=bcrypt.hashpw(password_g.encode(), bcrypt.gensalt())
        )
        db.session.add(u)
        try:
            db.session.commit()
            message = 'Your data is saved'
        except exc.SQLAlchemyError:
            return render_template('sign_up.html', message='Incorect email or username')
    return render_template('sign_up.html', message=message)  


@app.route('/sign_in/', methods=['post', 'get'])
def login():
    message = ''    
    if request.method == 'POST':    
        email = request.form.get('email') 
        password = str(request.form.get('password'))
        query_email_and_password = db.session.query(UsersInfo.user_login, UsersInfo.email, UsersInfo.user_password) \
            .filter(UsersInfo.email == email) \
            .first()
        if check_password(password, query_email_and_password[2]):
            session['name_usr'] = query_email_and_password[0]
            logging.info("User {} log in".format(session.get('name_usr')))
            session.modified = True
            return redirect("/machines")
        else:
            return redirect("/sign_in")
    else:
        message = 'Input email and password'     
    return render_template('sign_in.html', message=message)