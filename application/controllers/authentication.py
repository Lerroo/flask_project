from flask import Flask, request, redirect, render_template, url_for
from sqlalchemy import exc

import bcrypt
import os
import sys
import logging

sys.path.append(os.path.abspath('../../'))
from application import db, app
from application.models import UsersInfo
from application.services.utils import valudate_values, ValidationException
from application.services.user import password_enc, email_and_password_valid, token_create

@app.route('/sign_up/', methods=['get'])
def sign_up_get():
    return render_template('sign_up.html', message='Input your personal data')  


@app.route('/sign_up/', methods=['post'])
def sign_up():
    try:
        user_dict = request.form.to_dict()
        if valudate_values(user_dict):
            password_enc(user_dict).update({'token':token_create()})
            UsersInfo(**user_dict).add()
            return render_template('sign_up.html', message='Your data is saved')
    except ValidationException as error:
        return render_template('sign_up.html', message=error)
    

@app.route('/sign_in/', methods=['get'])
def login_get():
    return render_template('sign_in.html', message='Input email and password')


@app.route('/sign_in/', methods=['post'])
def login():
    try:
        form_dict = request.form.to_dict()
        if valudate_values(form_dict):
            if email_and_password_valid(form_dict):
                return redirect("/machines")
    except ValidationException as error:
        return render_template('sign_in.html', message=error)