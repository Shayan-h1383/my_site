from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ReviewForm(FlaskForm):
    content = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Save')
    
class RegistrationForm(FlaskForm):
    # Username field with a maximum length of 20 characters
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])

    # Password field with a maximum length of 20 characters
    password = PasswordField('Password', validators=[DataRequired(), Length(max=20)])
    
    email = StringField('Email', validators=[DataRequired(), Length(max=120), Email()])
    
    
