import os
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'hard to guess string'#
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class DebagConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.basedir, '1.db')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.basedir, '1.db')



