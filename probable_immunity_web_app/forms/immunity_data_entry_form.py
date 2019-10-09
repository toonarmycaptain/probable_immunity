"""Main immunity data entry form. Container for illness sub-forms."""

import datetime

from flask_wtf import FlaskForm
from wtforms import (SubmitField,
                     validators,
                     )
from wtforms.fields.html5 import IntegerField


from probable_immunity_web_app.forms import custom_validators

current_year: int = datetime.date.today().year  # Returns 4 digit year.


class ImmunityDataEntryForm(FlaskForm):
    birth_year = IntegerField(
        'Birth year:',
        [
            custom_validators.Year(
                min_year=1000,
                max_year=current_year,
                message=f'Birth year must be a 4 digit integer less than {current_year}.'),
            validators.InputRequired(message='Birth year required.'),
        ],
    )

    submit = SubmitField('Submit')
