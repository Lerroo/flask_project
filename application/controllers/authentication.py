from flask import Flask, request, redirect, render_template, url_for
from sqlalchemy import exc

import bcrypt
import os
import sys
import logging

sys.path.append(os.path.abspath('../../'))
from application import db, app
from application.models import UsersInfo
from application.services.utils import convert_to_dict_values, ValidationException
from application.services.user import password_enc, email_and_password_valid

@app.route('/sign_up/', methods=['get'])
def sign_up_get():
    return render_template('sign_up.html', message='Input your personal data')  


@app.route('/sign_up/', methods=['post'])
def sign_up():
    try:
        list_v = password_enc(convert_to_dict_values(request.form.to_dict()))
        UsersInfo(**list_v).add()
        return render_template('sign_up.html', message='Your data is saved')
    except ValidationException as error:
        return render_template('sign_up.html', message=error)
    

@app.route('/sign_in/', methods=['get'])
def login_get():
    return render_template('sign_in.html', message='Input email and password')


@app.route('/sign_in/', methods=['post'])
def login():
    try:
        if email_and_password_valid(convert_to_dict_values(request.form.to_dict())):
            return redirect("/machines")
    except ValidationException as error:
        return render_template('sign_in.html', message=error)