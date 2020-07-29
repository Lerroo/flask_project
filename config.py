import os
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'hard to guess string'#
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bd.db')


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'sqlite:///' + os.path.join(Config.basedir, 'bd.db')



