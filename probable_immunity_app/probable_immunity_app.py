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


@app.route('/hello')
def hello_world():
    return 'Hello World!'


immunity_app_bp = Blueprint('immunity_app', __name__, url_prefix='/immunity_app')


@immunity_app_bp.route('/measles_immunity', methods=('GET', 'POST'))
def measles_immunity():  # prototype with measles, expand to multiple illnesses, ie def immunities()
    if request.method == 'POST':
        birth_year = request.form['birth_year']
        on_time_measles_vaccinations = request.form['on_time_measles_vaccinations']
        error = None

        # Handle unentered values.
        if not birth_year:
            error = 'Birth year required.'
        elif not on_time_measles_vaccinations:
            error = 'Number of measles immunisations before age six needed, if none, select "0"'
        # Handle bad data.
        elif birth_year and on_time_measles_vaccinations:
            try:
                # Handle decimals by first converting str to int.
                session['birth_year'] = int(float(birth_year))
            except ValueError:
                error = 'Birth year must be a number.'

            try:
                # Handle decimals by first converting str to int (eg '2.0' -> 2. Rounds down.
                session['on_time_measles_vaccinations'] = int(float(on_time_measles_vaccinations))
            except ValueError:
                error = 'Number of vaccinations must be a number.'

        if error is None:
            return redirect(url_for('immunity_app.measles_immunity_results'))
        flash(error)

    return render_template('immunity_app/measles.html')


@immunity_app_bp.route('measles_immunity/results')
def measles_immunity_results():
    if not isinstance(session['birth_year'], int):
        raise ValueError
    if not isinstance(session['on_time_measles_vaccinations'], int):
        raise ValueError
    probability_of_immunity, message = measles.immunity(session['birth_year'], session['on_time_measles_vaccinations'])

    return render_template('immunity_app/measles_results.html',
                           probability_of_immunity=probability_of_immunity,
                           message=message,
                           )


if __name__ == '__main__':
    app.run()
