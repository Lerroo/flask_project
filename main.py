from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import bcrypt

from models import users_info
from config import db, app, local_salt

def enc(x, y):
    return bcrypt.hashpw(x, y)

@app.route('/sign_up/', methods=['post', 'get'])
def sign_up():
    message = 'Input your personal data'
    if request.method == 'POST':
        user_g = request.form.get('user') 
        email_g = request.form.get('email')  
        password_g = request.form.get('password')
        if not user_g or not email_g or not password_g:
            return render_template('sign_up.html', message='Incorect email or username')
        u = users_info(
            user_login=user_g,
            email=email_g, 
            user_password=enc( \
                enc(password_g.encode(), local_salt), 
                bcrypt.gensalt()
                )
            )
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
        query_email_and_password = db.session.query(users_info.email, users_info.user_password) \
            .filter(users_info.email == email) \
            .first()
        if query_email_and_password:
            hash_password = query_email_and_password[1]
            if bcrypt.checkpw(enc(password.encode(), local_salt), hash_password):
                message = "Correct"
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