from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, EmailField
from wtforms.validators import DataRequired, ValidationError, Optional
from flask_wtf.file import FileField, FileAllowed
from app import db
import sqlalchemy as sa
from app.models import User


class CardForm(FlaskForm):
    verb = StringField('Phrasal Verb', validators=[DataRequired()])
    meaning = StringField('Meaning', validators=[DataRequired()])
    example1 = StringField('Examples', validators=[DataRequired()])
    example2 = StringField('Examples', validators=[Optional()])
    example3 = StringField('Examples', validators=[Optional()])
    image_url = FileField('Upload Image', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    submit = SubmitField('Add')
    
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = db.session.scalar(
            sa.select(User).where(
                User.username == username.data
            )
        )
        if user is not None:
            raise ValidationError('Please use a different username')
        
    def validate_email(self, email):
        user = db.session.scalar(
            sa.select(User).where(
                User.email == email.data
            )
        )
        if user is not None:
            raise ValidationError('Email is already in use!')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')