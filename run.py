from flask import Flask, render_template
from datetime import datetime
import logging
import sys

from application import db, app
from application.controllers import authentication, machines


@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def forbidden(error):
    return render_template('404.html',message=error)

@app.route('/')
def index():
    return render_template('index.html', message='Сhoose your direction.')  

if __name__ == "__main__":
    file_name = 'logs/log_'+str(datetime.now().strftime("%Y-%m-%d"))+'.log'
    file_log = logging.FileHandler(file_name)
    console_out = logging.StreamHandler()
    logging.basicConfig(
        handlers=(file_log, console_out),
        level=logging.INFO)
    db.create_all()
    app.run()