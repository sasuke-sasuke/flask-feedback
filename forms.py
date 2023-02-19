from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, SelectField, PasswordField, EmailField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, AnyOf, Length

class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=25)])
    email = EmailField('Email', validators=[InputRequired(), Length(min=5, max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=30)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=25)])

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    content = StringField('Content', validators=[InputRequired()])