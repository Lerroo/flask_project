from flask import Flask, request, abort, render_template, session, make_response

from datetime import datetime
import sys
import os

from ..db_app import app, db
from ..models import Type

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


def valudate_values(valudate_dict):
    for k, v in valudate_dict.items():
        if v == '':
            raise (ValidationException(k))
    return valudate_dict


def json_validate(dict_json, dict_len):
    if valudate_values(dict_json) and len(dict_json)==dict_len:
        return dict_json
    return False


@app.errorhandler(400)
def forbidden(error):
    return make_response('Bad Request', 400)


@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def forbidden(error):
    return render_template('404.html', message=error)


@app.route('/')
def index():
    return render_template('index.html', message='Сhoose your direction.')
