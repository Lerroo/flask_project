from main import db

class users_info(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_login = db.Column(db.String(64), index = True, unique = True)
    user_password = db.Column(db.String(120), index = True, unique = True)
    email = db.Column(db.String(120),index = True, unique = True )



def init_db():
    

    # Create a test user
    new_user = users_info(user_login='us22g3', user_password='passwo22_g3', email='ema222_3g' )
    db.session.add(new_user)
    db.session.commit()


if __name__ == '__main__':
    init_db()