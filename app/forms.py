from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DecimalField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User
from wtforms.fields import DateTimeField

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('donor', 'Donor'), ('volunteer', 'Volunteer'), ('admin', 'Admin')], default='donor')
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')

class DonationForm(FlaskForm):
    type = SelectField('Donation Type', choices=[('monetary', 'Money'), ('goods', 'Goods/Items')])
    amount = DecimalField('Amount (if monetary)', validators=[DataRequired()], default=0)
    items = TextAreaField('Items Description (if goods)')
    ngo = SelectField('Select NGO', coerce=int)
    submit = SubmitField('Make Donation')

class PickupRequestForm(FlaskForm):
    ngo = SelectField('Select NGO', coerce=int, validators=[DataRequired()])
    address = TextAreaField('Pickup Address', validators=[DataRequired()])
    items = TextAreaField('Items Description', validators=[DataRequired()])
    pickup_time = DateTimeField('Preferred Pickup Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Request Pickup')

class NGORegistrationForm(FlaskForm):
    name = StringField('Organization Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = TextAreaField('Address', validators=[DataRequired()])
    description = TextAreaField('Organization Description', validators=[DataRequired()])
    documents = FileField('Registration Documents')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register NGO') 
