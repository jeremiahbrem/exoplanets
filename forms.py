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

class SelectListForm(FlaskForm):
    """Form for creating new list"""    

    lists = SelectField("Select List", coerce=int)

class SearchForm(FlaskForm):
    """Form for searching planets by parameter."""

    parameter = SelectField('Search by',
        choices=[('all', 'All'), ('habitable', 'Habitable Zone'), ('pl_masse', 'Planet Mass'), 
            ('pl_pnum', 'Number of Planets in System'), ('pl_rade', 'Planet Radius'), 
            ('pl_orbsmax', 'Planet Orbit'), ('pl_name', 'Planet Name'), ('pl_hostname', 'Star Name'),
            ('st_dist', 'Distance'), ('st_spstr', 'Spectral-Type'), ('st_mass', 'Solar Mass'), 
            ('st_rad', 'Solar Radius'), ('st_teff', 'Solar Surface Temp'), ('st_bmvj', 'Solar B-V Color Index'), 
            ('st_optmag', 'Star Optical Magnitude')]
        )

    search_input = StringField("Search input", validators=[Optional()])
    min_num = FloatField("Min", validators=[Optional()])
    max_num = FloatField("Max", validators=[Optional()])