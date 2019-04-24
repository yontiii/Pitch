from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required
from ..models import User

# views

@main.route('/')
def index():
    
  return render_template('index.html')  

@main.route('/pitch')
@login_required
def pitch():
    
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