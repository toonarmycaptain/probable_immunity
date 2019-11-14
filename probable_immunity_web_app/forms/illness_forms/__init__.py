"""
Individual illness forms and validation code.

Import into __init__ to provide flat API - illness_forms.xyz.
"""

from .measles_form import (Measles,
                           extract_measles_form_data,
                           )
from .mumps_form import (Mumps,
                         extract_mumps_form_data,
                         )

from .rubella_form import (Rubella,
                           extract_rubella_form_data,
                           )
