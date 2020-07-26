from flask import Flask, render_template
from datetime import datetime
import logging
import sys

from application import db, app
from application.controllers import authentication, machines
from application.API import API

if __name__ == "__main__":
    file_name = 'logs/log_'+str(datetime.now().strftime("%Y-%m-%d"))+'.log'
    file_log = logging.FileHandler(file_name)
    console_out = logging.StreamHandler()
    logging.basicConfig(handlers=(file_log, console_out), level=logging.INFO)
    db.create_all()
    app.run()