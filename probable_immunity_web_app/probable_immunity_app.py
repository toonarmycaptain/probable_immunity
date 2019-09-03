from flask import (Blueprint,
                   flash,
                   Flask,
                   redirect,
                   request,
                   render_template,
                   session,
                   url_for,
                   )

from probable_immunity_web_app.illness_config import illnesses

app = Flask(__name__)

# app.secret_key = os.urandom(32)


immunity_app_bp = Blueprint('immunity_app', __name__, url_prefix='/')


@immunity_app_bp.route('/immunity/', methods=('GET', 'POST'))
def immunity():
    if request.method == 'POST':
        birth_year = request.form['birth_year']
        on_time_measles_vaccinations = request.form['on_time_measles_vaccinations']
        error = None

        # Handle unentered values.
        if not birth_year:
            error = 'Birth year required.'
        elif not on_time_measles_vaccinations:
            error = 'Number of measles immunisations before age six needed, if none, enter 0.'
        # Handle bad data.
        elif birth_year and on_time_measles_vaccinations:
            error_str = ''  # Use str to allow concatenation
            try:
                # Handle decimals by first converting str to int.
                session['birth_year'] = int(float(birth_year))
            except ValueError:
                error_str = 'Birth year must be a number.\n'

            try:
                # Handle decimals by first converting str to int (eg '2.0' -> 2. Rounds down.
                session['measles'] = {'on_time_measles_vaccinations': int(float(on_time_measles_vaccinations))}
            except ValueError:
                error_str += 'Number of vaccinations must be a number.'

            if error_str:
                error = error_str

        if error is None:
            return redirect(url_for('immunity_app.immunity_results'))
        flash(error)

    return render_template('immunity_app/take_data.html', illnesses=illnesses)


@immunity_app_bp.route('/immunity/results/')
def immunity_results():
    for illness in illnesses:
        result_data = {}
        try:
            result_data[illness] = {**illnesses[illness]['immunity'](birth_year=session['birth_year'],
                                                                     **session[illness])
                                    }
        except (ValueError, TypeError):  # -> raise this in immunity() pass on TypeError also.
            result_data[illness] = {f'probability_of_{illness}_immunity': 'Unknown',
                                    'content_templates': ['immunity_results_error_message']}
        except KeyError:
            return redirect(url_for('immunity_app.immunity'), code=302)
        return render_template('immunity_app/immunity_results.html',
                               illnesses=illnesses,
                               **result_data,  # Dict form {illness: {k, v}, } - (whatever key-value each illness needs}
                               )


if __name__ == '__main__':
    app.run()



"""
have session[illness] = {'data key': data}
so each illness' data_dict is under it's own key in the session dict. 


def multi_immunity_results():
    # the alternative to this would be to abstract each illness separately, but
    # since this will probable all have a probability and a message, it might
    # be easier to use a * expansion, or simply
    # probability, message = immunity()


    for illness in illnesses:
        try:
            result_data[illness] = {**illness[immunity]()}
        except (ValueError, TypeError):  #-> raise this in immunity() pass on TypeError also.
            result_data[illness] = illnesses[illness]['error message']
        except KeyError:
            return redirect(url_for('immunity_app/immunity'), code=302)
        return render_template('immunity_app/immunity_results.html',
                               illnesses=illnesses,
                               **result_data, # then use dict of form {illness: (whatever key-value each illness needs}
                               )
                                # the alternative result_data = {**illness[immunity]() would require non duplicate keys
                                # from each illness - eg returning measles_probability_of_immunity rather than immunity_probability
                                # and probably be more error prone. result_data['birth_year'] can still be a key.
                                # It might be advisable/possible to make this dict a class with validation, but this might not wash with passing it to a jinja template.
# We can test the individual illness/templates by mocking illnesses in probable_immunity_app.py

Better to use wtf forms in the immunity/take_data view, and use error handling in the various illness.immunity functions
to handle Value/Type Errors:


Alternative implementation that will allow custom error messages to come from illness modules:
for illness in illnesses:
    try:
        result_data[illness] = {**illness[immunity]()} or even: result_data[illness] = {**illness[immunity](**session[illness])} 
    except (ValueError, TypeError) as error:  # -> raise this in immunity() pass on TypeError also.
        result_data[illness] = str(error)
    except KeyError:
        return redirect(url_for('immunity_app/immunity'), code=302)

# error demo:
# >>>def error_raise(a):
# ...    if isinstance(a, str):
# ...        raise ValueError('a was a string')
# ...    if isinstance(a, int):
# ...        raise TypeError('a was an int')
# ...    print('a was a float')
#
# # you can assign this error to a variable
# >>>try:
# ...    error_raise('a')
# ...except (TypeError, ValueError) as e:
# ...    g = e
#
# >>>g
# ValueError('a was a string')
# # You can also cast to string and pass on:
# >>>try:
# ...    error_raise('a')
# ...    g = str(e)
#
# >>>g
# 'a was a string'



WITH WT FORMS
store the subform in illnesses eg illnesses['measles']['form']

-then render the illness form in the in the illness template:
https://flask.palletsprojects.com/en/1.0.x/patterns/wtforms/
% from "_formhelpers.html" import render_field %}
<form method=post>
  <dl>
    {{ render_field(form.username) }}
    {{ render_field(form.email) }}
    {{ render_field(form.password) }}
    {{ render_field(form.confirm) }}
    {{ render_field(form.accept_tos) }}
  </dl>
  <p><input type=submit value=Register>
</form>


-then in the immunity route:
for illness in illnesses:
    if not form.illnesses['measles']['form'].validate()
        # add illness to error str
if error - flash error
else redirect to results
"""
