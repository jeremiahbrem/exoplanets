"""Forms for playlist app."""

from flask import g
from wtforms import FloatField, SelectField, StringField
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
    password = StringField("Password", validators=[InputRequired(), Length(
                                                                min=8, 
                                                                message="Minimum password length is 8 characters."
                                                                )
                                                                ])

    email = StringField("Email", validators=[InputRequired(), Email(), check_unique_email])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("First Name", validators=[InputRequired()])

class SearchForm(FlaskForm):
    """Form for searching planets by parameter."""

    parameters = SelectField('Parameters',
        choices=[('all', 'All'), ('pl_masse', 'Planet mass'), ('pl_rade', 'Planet radius'),
            ('pl_orbsmax', 'Planet orbit'), ('st_dist', 'Distance'), ('st_spstr', 'Spectral-type'),
            ('st_mass', 'Solar mass'), ('st_rad', 'Solar radius'), ('st_teff', 'Solar temp'),
            ('st_bmvj', 'Solar color'), ('st_optmag', 'Solar magnitude')]
        )

    min = FloatField("Min")
    max = FloatField("Max")

        