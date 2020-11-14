from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed   # restricts which types of files are allowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
# note: pip install wtforms[email] must be done separately if done on new system
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import Patient, Doctor


# instances of these classes are created in the route
class PatientRegistrationForm(FlaskForm):
    # format: type of field (label, validators=[])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Patient.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Patient.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


# instances of these classes are created in the route
class DoctorRegistrationForm(FlaskForm):
    # format: type of field (label, validators=[])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    doctor_type = StringField('Specialization', validators=[DataRequired()])
    payment = StringField('Pricing', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Patient.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Patient.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ReportForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class UserTypeForm(FlaskForm):
    user_type = SelectField('User Type', choices=[('Patient', 'Patient'), ('Doctor', 'Doctor')])
    submit = SubmitField('Select')


class ChatForm(FlaskForm):
    text = StringField('Enter Text Here...')
    submit = SubmitField('Select')