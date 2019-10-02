"""
Illness objects and data store.


Illness objects have an API contract requiring them to provide:

    .name attr string

    .immunity() function
    returning a Dict {f'probability_of_{illness}_immunity': float, 'content_templates': List(str)}

    .form attr returning a WTForm to be given to the data entry template.

    .extract_data(form)
    returning a dict {illness_data: values} from form data to store in session.
        NB dict will be added as value for key in session Session['illness name']


    If needed, we could implement something like:
    .validate_form_data(form) function taking form and validating arguments for that illness,
        returning any errors as non-empty string, otherwise returning empty string.
        - in the case that Flask-WTF is not sufficient.
"""

from .measles import Measles
from .mumps import Mumps
