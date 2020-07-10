import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bd.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.debug = True
app.config.from_object('config')
app.config['SECRET_KEY'] = 'hard to guess string'

db = SQLAlchemy(app)
db.create_all()