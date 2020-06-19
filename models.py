from config import db

class users_info(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_login = db.Column(db.String(64), index = True, unique = True)
    user_password = db.Column(db.String(120), index = True)
    email = db.Column(db.String(120),index = True, unique = True )