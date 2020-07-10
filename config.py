import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///'
    SECRET_KEY = 'hard to guess string'#
    basedir = os.path.abspath(os.path.dirname(__file__))

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DB_SERVER = 'localhost'
    TRACK_MODIFICATIONS = False
    DEBUG = True
    DATABASE_URI = 'sqlite:///' + os.path.join(Config.basedir, 'bd.db')