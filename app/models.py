from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You can not read the password attribute')
    
    
    @password.setter
    def passsword(self,passsword):
        self.pass_secure = generate_password_hash(passsword)
    
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)
    
    def __repr__(self):
        return f'User {self.username}'
    
class Role(db.Model):
    
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User' , backref = 'role',lazy = 'dynamic')
    
    def __repr__(self):
        return f'User {self.name}'
    
    
    
    