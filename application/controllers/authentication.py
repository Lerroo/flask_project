from flask import Flask, request, redirect, render_template, url_for
from sqlalchemy import exc

import bcrypt
import os
import sys
import logging


from ..services.user import prepare_user, validate_email_and_password, token_create
from ..services.utils import valudate_values, ValidationException
from ..db_app import db, app
from ..models import UsersInfo


@app.route('/sign_up/', methods=['get'])
def sign_up_get():
    return render_template('sign_up.html', message='Input your personal data')  


@app.route('/sign_up/', methods=['post'])
def sign_up():
    try:
        user_dict = request.form.to_dict()
        if valudate_values(user_dict):
            UsersInfo(**prepare_user(user_dict)).add()
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
            if validate_email_and_password(form_dict):
                return redirect("/machines")
    except ValidationException as error:
        return render_template('sign_in.html', message=error)