from flask import Flask, render_template
from datetime import datetime
import logging
import sys


# import application.API.demo
# import application.API.API as ap
# import application.services.user
# # import application.services.utils
from application.db_app import app, db



if __name__ == "__main__":
    file_name = 'logs/log_'+str(datetime.now().strftime("%Y-%m-%d"))+'.log'
    file_log = logging.FileHandler(file_name)
    console_out = logging.StreamHandler()
    format_stdout = u'%(levelname)-8s [%(asctime)s]: %(message)s'
    logging.basicConfig(handlers=(file_log, console_out), level=logging.INFO, format=format_stdout, datefmt='%d-%b-%y')
    db.create_all()
    app.run()

print(ap.apio())