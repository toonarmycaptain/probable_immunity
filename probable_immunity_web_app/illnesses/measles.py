from illnesses import measles
from probable_immunity_web_app.forms import illness_forms


from .illness import Illness

Measles = Illness(name='measles',
                  immunity=measles.immunity,
                  wt_form=illness_forms.Measles,
                  form_data_extractor=illness_forms.extract_measles_form_data,
                  )
