from illnesses import rubella
from probable_immunity_web_app.forms import illness_forms

from .illness import Illness

Rubella = Illness(name='rubella',
                  immunity=rubella.immunity,
                  wt_form=illness_forms.Rubella,
                  form_data_extractor=illness_forms.extract_rubella_form_data,
                  )
