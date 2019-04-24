from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    pitches = db.relationship('Pitch', backref = 'user' ,lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You can not read the password attribute')
    
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return f'User {self.username}'
    
class Pitch(db.Model):
    
    __tablename__ = 'pitches'
    
    id = db.Column(db.Integer,primary_key = True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    pitch = db.Column(db.String(255))
    title = db.Column(db.String(255))
    date = db.Column(db.Datetime, default = datetime.utcnow)
    vote_count = db.Column(db.Integer)
    
    def save_pitch(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_pitches(cls,id):
        pitches = Pitch.query.filter_by(pitch_id = id).all()
        return pitches        
    
    def __repr__(self):
        return f'Pitch {self.pitch}'
    

    
    
    