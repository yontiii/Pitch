from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField("Say Something Interesting", validators = [Required()])
    submit = SubmitField('Submit')


class PitchForm(FlaskForm):
    title = StringField("Title",validators = [Required()] )
    author = StringField('Author', validators=[[Required()]])
    pitch = TextAreaField("Enter Your Pitch" , validators=[Required()])
    
    
    