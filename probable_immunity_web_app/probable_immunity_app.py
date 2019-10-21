from flask import (Blueprint,
                   current_app,
                   redirect,
                   request,
                   render_template,
                   session,
                   url_for,
                   )
from wtforms import FormField

import probable_immunity_web_app.forms.immunity_data_entry_form as forms

from probable_immunity_web_app.illness_config import Illnesses

immunity_app_bp = Blueprint('immunity_app', __name__, url_prefix='/')


@immunity_app_bp.route('/immunity/', methods=('GET', 'POST'))
def immunity():
    illnesses = Illnesses(current_app.config['ILLNESS_LIST'])
    # Initialise form from config:
    for illness in illnesses:
        setattr(forms.ImmunityDataEntryForm, illness.name, FormField(illness.form))
    # Set form
    form = forms.ImmunityDataEntryForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Place validated data in session.
            session['birth_year'] = form.birth_year.data
            for illness in illnesses:
                # Store data in session.
                session[illness.name] = illness.extract_data(form)

            if not form.errors:
                return redirect(url_for('immunity_app.immunity_results'))
        # else:
        # Templates will render error messages from form.errors.

    return render_template('immunity_app/take_data.html', illnesses=illnesses.names, form=form)


@immunity_app_bp.route('/immunity/results/')
def immunity_results():
    illnesses = Illnesses(current_app.config['ILLNESS_LIST'])
    result_data = {}
    for illness in illnesses:
        try:
            result_data[illness.name] = {**illness.immunity(birth_year=session['birth_year'],
                                                            **session[illness.name])
                                         }
        except (ValueError, TypeError):  # -> raise this in immunity() pass on TypeError also.
            # Display error for individual illness if error occurred on validated data inside immunity()
            result_data[illness.name] = {f'probability_of_{illness.name}_immunity': 'Unknown',
                                         'content_templates': ['immunity_results_error_message']}
        except KeyError:
            return redirect(url_for('immunity_app.immunity'), code=302)

    return render_template('immunity_app/immunity_results.html',
                           illnesses=illnesses.names,
                           **result_data,  # Dict form {illness: {k, v}, } - (whatever key-value each illness needs}
                           )
