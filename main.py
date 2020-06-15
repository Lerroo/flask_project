from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import bcrypt

from models import users_info
from config import db, app

@app.route('/sign_up/', methods=['post', 'get'])
def sign_up():
    message = 'Input your personal data'
    if request.method == 'POST':
        user_g = request.form.get('user') 
        email_g = request.form.get('email')  
        password_g = bcrypt.hashpw(request.form.get('password').encode(), bcrypt.gensalt())
        print("{}:{}:{}".format(user_g, email_g, password_g))
        db.create_all()
        u = users_info(user_login=user_g, email=email_g, user_password=password_g)
        db.session.add(u)
        try:
            db.session.commit()
            message = 'Your data is saved'
        except exc.SQLAlchemyError:
            return render_template('sign_up.html', message='Incorect email or username')
    return render_template('sign_up.html', message=message)  

@app.route('/sign_in/', methods=['post', 'get'])
def login():
    message = ''    
    if request.method == 'POST':    
        email = request.form.get('email')  # запрос к данным формы
        password = str(request.form.get('password'))
        if password != "" and email != "":
            query_email_and_password = dict(db.session.query(users_info.email, users_info.user_password) \
                .filter(users_info.email == email))
            print(query_email_and_password)
            hash_password = query_email_and_password.get(email, b"000")
            if bcrypt.checkpw(password.encode(), hash_password):
                message = "Correct"
            else:
                message = "Wrong email or password" 
        else:
            message = "Wrong email or password" 
    if request.method == 'GET':
        message = 'Input email and password'     
    return render_template('sign_in.html', message=message)

@app.route('/')
def index():
    return render_template('index.html', message='Сhoose your direction.')  

if __name__ == "__main__":
    app.run()