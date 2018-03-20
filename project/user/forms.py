# project/user/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length, EqualTo

from project.models import User

# A form class to change password
class ChangePasswordForm(FlaskForm):
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])
    confirm = PasswordField('Repeat password', validators=[InputRequired(), EqualTo('password', message='Passwords must match.')])

# A form class for login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])
    remember = BooleanField('remember me')

# A form class for user registration. Validates existing user through email.
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    confirm = PasswordField('Repeat password', validators=[InputRequired(), EqualTo('password', message='Passwords must match.')])
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=80)])

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True