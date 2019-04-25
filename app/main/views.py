from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch,Comment
from .. import db,photos
from .forms import PitchForm,UpdateProfile,CommentsForm

# views

@main.route('/')
def index():
    
  return render_template('index.html')  

@main.route('/pitch', methods = ['GET','POST'])
@login_required
def pitch():
  pitches = Pitch.query.all()
  form = PitchForm()
  
  if form.validate_on_submit():
    # update new Pitch
    title = form.title.data
    pitch = form.pitch.data
    upvote = 0
    downvote = 0
    
    # updated pitch instance
    new_pitch = Pitch(title = title, pitch = pitch, upvote = upvote, downvote = downvote, current_user = current_user)
    new_pitch.save_pitch()    
    return render_template('pitch.html' , form = form, pitches = pitches)
  
  
@main.route('/comments/<int:id>', methods = ['GET','POST'])
@login_required
def comments(id):
  pitch = Pitch.query.get_or_404(id)
  comment = Comment.query.all()
  commentform = CommentsForm()
  
  if request.args.get("upvote"):
    pitch.upvote = pitch.upvote+1
    
    db.session.add(pitch)
    db.session.commit()
    
    return redirect("/comments/{pitch_id}".format(pitch_id=pitch.id))
  
  elif request.args.get("downvote"):
    pitch.downvote = pitch.downvote + 1
    
    db.session.add(pitch)
    db.session.commit()
    
    return redirect("/comments/{pitch_id}".format(pitch_id=pitch.id))
  
  if form.validate_on_submit():
    comment = form.comment.data
    
    new_comment = Comment(id=id, comment= comment,user_id = current_user.id)
    
    new_comment.save_comment()
    
    return redirect(url_for("main.comments", id = id))
    comments = Comment.query.all()
    
    return render_template("comments.html",comment = comment, pitch = pitch, commentform = commentform, comments= comments)  
  
  
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

