#Import frameworks
from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import Email, DataRequired, Regexp, Length, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from datetime import datetime, timedelta

#Import User model
from models import User

#Checks if a user exists where the username is the same as the input of the field.
#If so raise the validation error.
def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User already exists.')


#Checks if a user exists where the email is the same as the input of the field.
#If so raise the validation error.
def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email exists.')

def date_in_future(form, field):
    try:
        val = field.data
    except ValueError:
        val = None
    if val:
        if val < datetime.now().date():
            raise ValidationError('Selected date is in the past.')

def date_is_weekday(form, field):
    if (field.data).weekday() > 4:
        raise ValidationError('Selected date is on a weekend.')

def date_too_far(form, field):
    if (field.data) > (datetime.now() + timedelta(days=31)).date():
        raise ValidationError('Cannot book that far in advance.')

#Creates a registration form with validated fields.
class RegistrationForm(Form):
    username = StringField(
        #Give the username field a label of 'username'.
        'Username',
        #Valid if there is data in the field,
        #the username is of the format specified
        #and the username doesn't already exist
        validators=[
            DataRequired(),
            Regexp(
                r'[a-z]+\.[a-z]+',
                message=("Username should be first name followed "
                        "by dot (.) followed by surname (lowercase).")
            ),
            name_exists
        ]
    )
    email = StringField(
        #Set the label to 'email'
        'Email',
        validators=[
            #Valid if data is present
            #An Email has been entered
            #The email address ends in '@ridgewoodschool.co.uk'
            #The email isn't already assigned to a user
            DataRequired(),
            Email(),
            Regexp(
                r'[a-z]+\.[a-z]+@ridgewoodschool.co.uk',
                message="Email should be in the format 'first_name.surname@ridgewoodschool.co.uk'."
            ),
            email_exists
        ]
    )
    password = PasswordField(
        #Set the label to 'Password'
        'Password',
        validators=[
            #Valid if data is present
            #At least 5 characters input
            #Is equal to the confirmed password
            DataRequired(),
            Length(min=6),
            EqualTo('password2', message="Passwords must be equal.")
        ]
    )
    password2 = PasswordField(
        #Set label to 'Confirm Password'
        'Confirm Password',
        #Valid if data is present as only one password
        #needs full validation as they should be equal
        validators=[DataRequired()]
    )

#Form for when a user is already registered and wishes to login
class LoginForm(Form):
    #Login with username and password
    #Only validators required are DataRequired() as if the user has an account
    #these will already be validated
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

#Form for when a user is creating a booking
class BookingForm(Form):
    #Room property is a select field to choose from a variety of options
    #The first value in (value, pair) is the string to be stored in the DB
    #The paired value is the user facing string
    #The field is required
    room = SelectField(
        'Room',
        choices=[
            ('Library: Ground Floor', 'Library: Ground Floor'),
            ('Library: First Floor', 'Library: First Floor'),
            ('Social Area: First Floor', 'Social Area: First Floor'),
            ('F16', 'F16'),
            ('F19', 'F19'),
            ('F22', 'F22'),
            ('F23', 'F23'),
            ('F30', 'F30'),
            ('F59', 'F59'),
            ('F62', 'F62'),
            ('F76', 'F76')
            ],
        validators=[DataRequired()]
    )
    #Date field allows a date input in the format Y-M-D
    #Required field
    date = DateField(
        'Date',
        validators=[DataRequired(), date_in_future, date_is_weekday, date_too_far],
        format= '%Y-%m-%d'
    )
    #Allows the user to select a period in which they will use the computer
    #Required field
    period = SelectField(
        'Period',
        choices=[
            ('P1', 'Period 1'),
            ('P2', 'Period 2'),
            ('P3', 'Period 3'),
            ('P4', 'Period 4'),
            ('P5', 'Period 5')
        ],
        validators=[DataRequired()]
    )
    #Allows the user to enter their subject that they will be working on
    purpose = StringField(
        'Subject',
        validators=[DataRequired()]
    )
