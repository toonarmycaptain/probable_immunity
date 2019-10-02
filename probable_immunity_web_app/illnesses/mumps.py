from illnesses import mumps
from probable_immunity_web_app.forms import illness_forms


from .illness import Illness

Mumps = Illness(name='mumps',
                  immunity=mumps.immunity,
                  wt_form=illness_forms.Mumps,
                  form_data_extractor=illness_forms.extract_mumps_form_data,
                  )
