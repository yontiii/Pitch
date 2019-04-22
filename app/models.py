from . import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    pass_secure = db.Column(db.String(255))

    @property
    def passsword(self):
        raise AttributeError('You can not read the password attribute')
    
    
    
    
    def __repr__(self):
        return f'User {self.username}'
    
class Role(db.Model):
    
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User' , backref = 'role',lazy = 'dynamic')
    
    def __repr__(self):
        return f'User {self.name}'
    
    
    
    