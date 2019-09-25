"""Measles data entry form."""
from typing import Type

from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.html5 import IntegerField


class Measles(FlaskForm):
    on_time_measles_vaccinations = IntegerField(
        'Measles immunisations by age six:',
        [
            validators.NumberRange(
                min=0,
                max=None,
                message='Number of measles vaccinations by age six must be an integer ≥ 0.'),
            # Use InputRequired because DataRequired will return False for 0, see /github.com/wtforms/wtforms/issues/255
            validators.InputRequired(
                message='Please enter the number of measles vaccinations by age six, if none, enter 0.'),
        ],
    )


def extract_measles_form_data(form: Type[FlaskForm]) -> dict:
    return {'on_time_measles_vaccinations': int(form.measles.on_time_measles_vaccinations.data)}
