from illnesses import measles

from flask import (Blueprint,
                   flash,
                   Flask,
                   redirect,
                   request,
                   render_template,
                   session,
                   url_for,
                   )

app = Flask(__name__)


# app.secret_key = os.urandom(32)


immunity_app_bp = Blueprint('immunity_app', __name__, url_prefix='/')

illnesses = ['measles']


@immunity_app_bp.route('/immunity', methods=('GET', 'POST'))
def immunity():  # prototype with measles, expand to multiple illnesses, ie def immunities()
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


immunity_results_error_message = (
    b'<html>'
    b'<p>An error was encountered. Please try again.</p>'
    b'<p>Please raise an <a href="https://github.com/toonarmycaptain/probable_immunity/issues">issue on Github.</p>'
    b'</html>')


@immunity_app_bp.route('immunity/results')
def immunity_results():
    try:
        if not isinstance(session['birth_year'], int):
            raise ValueError
        if not isinstance(session['measles']['on_time_measles_vaccinations'], int):
            raise ValueError
    except ValueError:
        return immunity_results_error_message
    # If no session/keys, return to data entry page.
    except KeyError:
        return redirect(url_for('immunity_app.immunity'), code=302)

    # Measles
    probability_of_measles_immunity, measles_message = measles.immunity(session['birth_year'],
                                                                        session['measles']['on_time_measles_vaccinations'])

    return render_template('immunity_app/immunity_results.html',
                           illnesses=illnesses,
                           probability_of_measles_immunity=probability_of_measles_immunity,
                           measles_message=measles_message,
                           )


if __name__ == '__main__':
    app.run()
