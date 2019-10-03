"""Measles data entry form."""
from typing import Type

from flask_wtf import FlaskForm
from wtforms import validators, BooleanField
from wtforms.fields.html5 import IntegerField


class Mumps(FlaskForm):
    on_time_mumps_vaccinations = IntegerField(
        label='Mumps immunisations by age six:',
        validators=[
            validators.NumberRange(
                min=0,
                max=None,
                message='Number of mumps vaccinations by age six must be an integer ≥ 0.'),
            # Use InputRequired because DataRequired will return False for 0, see /github.com/wtforms/wtforms/issues/255
            validators.InputRequired(
                message='Please enter the number of mumps vaccinations by age six, if none, enter 0.'),
        ],
    )
    mumps_illness = BooleanField(label='Had a case of the measles:',
                                 false_values=("False",  # This is needed to use False bool in request tests.
                                               ),
                                 )


def extract_mumps_form_data(form: Type[FlaskForm]) -> dict:
    return {'on_time_mumps_vaccinations': int(form.mumps.on_time_mumps_vaccinations.data),
            'mumps_illness': form.mumps.mumps_illness.data}
