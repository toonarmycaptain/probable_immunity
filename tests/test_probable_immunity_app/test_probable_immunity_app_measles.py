import flask
import pytest

from werkzeug.datastructures import ImmutableMultiDict

from probable_immunity_web_app.illnesses import Measles

from tests.request_generator_helpers import flatten_dict


@pytest.mark.parametrize(
    'request_data',
    [  # 0 shots
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': '0'},
          }),
        ({'birth_year': '1957',
          'measles': {'on_time_measles_vaccinations': '0'},
          }),
        ({'birth_year': '1958',
          'measles': {'on_time_measles_vaccinations': '0'},
          }),
        ({'birth_year': '2011',
          'measles': {'on_time_measles_vaccinations': '0'},
          }),
        # 1 shot
        ({'birth_year': '1957',
          'measles': {'on_time_measles_vaccinations': '1'},
          }),
        ({'birth_year': '1958',
          'measles': {'on_time_measles_vaccinations': '1'},
          }),
        ({'birth_year': '2011',
          'measles': {'on_time_measles_vaccinations': '1'},
          }),
        # 2 shots
        ({'birth_year': '1957',
          'measles': {'on_time_measles_vaccinations': '2'},
          }),
        ({'birth_year': '1958',
          'measles': {'on_time_measles_vaccinations': '2'},
          }),
        ({'birth_year': '2011',
          'measles': {'on_time_measles_vaccinations': '2'},
          }),
        # >2 shots
        ({'birth_year': '1957',
          'measles': {'on_time_measles_vaccinations': '3'},
          }),
        ({'birth_year': '1958',
          'measles': {'on_time_measles_vaccinations': '7'},
          }),
        ({'birth_year': '2011',
          'measles': {'on_time_measles_vaccinations': '12'},
          }),
    ])
def test_immunity_session_contents_measles(app_specific_illnesses,
                                           request_data,
                                           monkeypatch):
    app = app_specific_illnesses(illnesses=[Measles])
    with app.test_client() as test_client:

        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

        assert test_client.get('immunity/').status_code == 200

        response = test_client.post(
            'immunity/', data=flat_request_data)

        assert flask.session['birth_year'] == int(request_data['birth_year'])
        assert flask.session['measles'] == {
            'on_time_measles_vaccinations': int(request_data['measles']['on_time_measles_vaccinations'])}

        # Ensure successful redirect to results in response.
        assert 'http://localhost/immunity/results/' == response.headers['Location']
