from webapp import db,app
from datetime import  datetime
from flask_login import UserMixin
from webapp import login
from werkzeug.security import check_password_hash ,generate_password_hash
from time import time
import jwt

class User(db.Model,UserMixin):
    id = db.Column (db.Integer , primary_key=True)
    username = db.Column (db.String(40),index=True,unique=True)
    email = db.Column(db.String(40), index=True, unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship ('Post',backref='author',lazy='dynamic')
    def __repr__(self):
        return '<Utilisateur {}>'.format(self.username)
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
    def set_password(self,t):
        self.password=generate_password_hash(t)

    def check_password(self,x):
        return check_password_hash(self.password,x)

    def get_reset_password_token(self,expires_in=600):
        return jwt.encode({'reset_password':self.id,'exp':time()+expires_in},
                          app.config ['SECRET_KEY'],algorithm='HS256').decode('utf-8')

    # verfier  le jeton
    @staticmethod
    def verify_reset_password_token(token):
            try:
                id = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
            except :
                return
            return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    used_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Post {}>'.format(self.body)
