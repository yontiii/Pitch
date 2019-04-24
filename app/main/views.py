from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required
from ..models import User,Pitch
from .. import db,photos
from .forms import PitchForm

# views

@main.route('/')
def index():
    
  return render_template('index.html')  

@main.route('/pitch')
@login_required
def pitch():
  form = PitchForm()
  
  if form.validate_on_submit():
    # update new Pitch
    title = form.title.data
    pitch = form.pitch.data
    upvote = 0
    downvote = 0
    new_pitch = Pitch(author = form.author.data, title = form.title.data, pitch = form.pitch.data)
    new_pitch.save_pitch()    
    return render_template('pitch.html')
  
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update', methods = ['GET','POST'])
@login_required
def update_profile(uname):
  user = User.query.filter_by(username = uname).first()
  
  if user is None:
    abort(404)
    
    form = update_profile()
    
    if form.validate_on_submit():
      user.bio = form.bio.data
      
      db.session.add(user)
      db.session.commit()
      
      return redirect(url_for('.profile', uname= user.username))
    
  return render_template('profile/update.html', form = form)


@main.route('/user/<uname>/update/pic', methods = ['POST'])
@login_required
def update_pic(uname):
  user = User.query.filter_by(username = uname).first()
  if 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path = f'photos/{filename}'
    user.profile_pic_path = path
    db.session.commit()
  
  
  return redirect(url_for('main.profile', uname = uname ))

