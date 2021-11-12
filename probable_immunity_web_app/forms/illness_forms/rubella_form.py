"""Rubella data entry form."""
from typing import Type

from flask_wtf import FlaskForm
from wtforms import validators, BooleanField
from wtforms import IntegerField


class Rubella(FlaskForm):
    rubella_vaccinations = IntegerField(
        label='Rubella immunisations:',
        validators=[
            validators.NumberRange(
                min=0,
                max=None,
                message='Number of rubella vaccinations must be an integer ≥ 0.'),
            # Use InputRequired because DataRequired will return False for 0, see /github.com/wtforms/wtforms/issues/255
            validators.InputRequired(
                message='Please enter the number of rubella vaccinations, if none, enter 0.'),
        ],
    )
    rubella_illness = BooleanField(label='Had a case of rubella:',
                                   false_values=("False",  # This is needed to use False bool in request tests.
                                                 ),
                                   )


def extract_rubella_form_data(form: Type[FlaskForm]) -> dict:
    return {'rubella_vaccinations': int(form.rubella.rubella_vaccinations.data),
            'rubella_illness': form.rubella.rubella_illness.data}
