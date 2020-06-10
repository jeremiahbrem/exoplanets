"""Forms for playlist app."""

from flask import g
from wtforms import FloatField, SelectField, StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, ValidationError, Length, Email
from models import User

def check_unique_username(form, field):
    """Checks for unique username is signing up"""

    if User.query.filter_by(username=field.data).first():
        raise ValidationError("Username already exists.")

def check_unique_email(form, field):
    """Checks for unique username is signing up"""

    if User.query.filter_by(email=field.data).first():
        raise ValidationError("Email already exists.")

class SignUpForm(FlaskForm):
    """Form for new user signup"""

    username = StringField("Username", validators=[InputRequired(), check_unique_username])
    password = PasswordField("Password", validators=[InputRequired(), Length(
                                                                min=8, 
                                                                message="Minimum password length is 8 characters."
                                                                )
                                                                ])

    email = StringField("Email", validators=[InputRequired(), Email(), check_unique_email])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("First Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging in"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

def check_unique_list(form, field):
    """Checks for unique user list name
    NOTE: Only needs to be unique to user; other users can have same list name"""

    lists = g.user.lists
    for user_list in g.user.lists:
        if user_list.name == field.data:
            raise ValidationError("List name already exists.")

class CreateListForm(FlaskForm):
    """Form for creating new list"""    

    name = StringField("List Name", validators=[InputRequired(), check_unique_list])
    description = StringField("Description", validators=[Optional()])

class SearchForm(FlaskForm):
    """Form for searching planets by parameter."""

    parameter = SelectField('Search by',
        choices=[('all', 'All'), ('habitable', 'Habitable zone'), ('pl_masse', 'Planet mass'), 
            ('pl_pnum', 'Number of planets in system'), ('pl_rade', 'Planet radius'), 
            ('pl_orbsmax', 'Planet orbit'), ('pl_name', 'Planet name'), ('pl_hostname', 'Star name'),
            ('st_dist', 'Distance'), ('st_spstr', 'Spectral-type'), ('st_mass', 'Solar mass'), 
            ('st_rad', 'Solar radius'), ('st_teff', 'Solar temp'), ('st_bmvj', 'Solar color'), 
            ('st_optmag', 'Solar magnitude')]
        )

    search_input = StringField("Search input")
    min_num = FloatField("Min", validators=[Optional()])
    max_num = FloatField("Max", validators=[Optional()])