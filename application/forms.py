from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from application.models import User



class NewUserForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-mail adress', validators=[DataRequired(), Email(message='The email adress is not correct!')])
    password = PasswordField('Pasword', validators=[DataRequired()])
    confirm_password = PasswordField('Password again',
                                     validators=[DataRequired(), EqualTo('password', message='The password does not mathch with the previous one')
                                                                       ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already used. Use another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email adress is already used. Use another one!')


class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Stay logged in')
    submit = SubmitField('Log in')