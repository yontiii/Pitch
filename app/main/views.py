from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required

# views

@main.route('/')
def index():
    
  return render_template('index.html')  

@main.route('/pitch')
@login_required
def pitch():
    
    return render_template('pitch.html')