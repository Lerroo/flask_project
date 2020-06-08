from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from app_main import db
import models



app = Flask(__name__)
app.debug = True
app.config.from_object('config')
app.config['SECRET_KEY'] = 'hard to guess string'
db = SQLAlchemy(app)

@app.route('/user/<id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)

@app.route('/career/')
def career():
    return 'Career Page'

@app.route('/feedback/')
def feedback():
    return 'Feedback Page'

@app.route('/sign_up/', methods=['post', 'get'])
def sign_up():
    message = 'Input your personal data'
    if request.method == 'POST':
        user_g = request.form.get('user') 
        email_g = request.form.get('email')  
        password_g = request.form.get('password')
        db.create_all()
        u = models.users_info(user_login=user_g, email=email_g, user_password=password_g)
        db.session.add(u)
        try:
            db.session.commit()
            message = 'Your data is saved'
        except exc.SQLAlchemyError:
            return render_template('sign_up.html', message='Incorect email or password or username')
    return render_template('sign_up.html', message=message)  

@app.route('/sign_in/', methods=['post', 'get'])
def login():
    message = ''
    
    if request.method == 'POST':
    
        email = request.form.get('email')  # запрос к данным формы
        password = request.form.get('password')
        email_all = db.session.query(models.users_info.email).all()
        print((str(email),),'::',email_all)
        if ((str(email),) in email_all):
            message = "Correct email and password"
            print('allala')
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