from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch,Review
from .. import db,photos
from .forms import PitchForm,UpdateProfile,CommentsForm

# views

@main.route('/')
def index():
  
  title = "The Pitch"
  
  return render_template('index.html', title = title)  

@main.route('/posts')
@login_required
def posts():
  pitches = Pitch.query.all()
 
  return render_template('posts.html', pitches = pitches)  

@main.route('/pitch', methods = ['GET','POST'])
@login_required
def pitch():

  pitch_form = PitchForm()

  
  if pitch_form.validate_on_submit():
    pitch_title = pitch_form.title.data
  
    pitch_body = pitch_form.pitch.data
    upvote = 0
    downvote = 0
    
    # updated pitch instance
    new_pitch = Pitch(pitch_title = pitch_title, pitch_body = pitch_body, upvote = upvote, downvote = downvote)
   
    
    new_pitch.save_pitch()
    return redirect(url_for('main.posts'))  
    
  return render_template('pitch.html' , pitch_form= pitch_form)
  
  
@main.route('/pitch_review/<int:id>', methods = ['GET','POST'])
@login_required
def pitch_review(id):
  pitch = Pitch.query.get_or_404(id)
  comments = Review.query.all()
  commentform = CommentsForm()
  
  if request.args.get("upvote"):
    pitch.upvote = pitch.upvote+1
    
    db.session.add(pitch)
    db.session.commit()
    
    return redirect("/pitch_review/{pitch_id}".format(pitch_id=pitch.id))
  
  elif request.args.get("downvote"):
    pitch.downvote = pitch.downvote + 1
    
    db.session.add(pitch)
    db.session.commit()
    
    return redirect("/pitch_review/{pitch_id}".format(pitch_id=pitch.id))
  
  if commentform.validate_on_submit():
    review = commentform.review.data
    
    new_review = Review(id=id, review= review,user_id = current_user.id)
    
    new_review.save_review()
    
    return redirect(url_for("main.pitch_review", id = id))
    

  return render_template("pitch_review.html",comments = comments, pitch = pitch, commentform = commentform)  
  
  
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

