from flask import Flask, request, abort, render_template, session

from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath('../../'))
from application import app
from application.models import Type

type_list = Type.query.all()


class ValidationException(Exception):
    def __init__(self, err):
        self.name = err

    def __str__(self):
        return 'error ' + self.name


def now_time_iso():
    return datetime.now().isoformat(sep='T', timespec="seconds")


def session_name():
    if not session.get('name_usr'):
        abort(401)
    return True


def convert_to_dict_values(values_form):
    for k, v in values_form.items():
        if v == '':
            raise (ValidationException(k))
    return values_form


@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def forbidden(error):
    return render_template('404.html', message=error)


@app.route('/')
def index():
    return render_template('index.html', message='Сhoose your direction.')
