"""
Test immunity app measles illness.


NB Since measles_illness is a checkbox, it is difficult to send invalid data, and
hence isn't always tested, or the value is omitted.

Generally, any value submitted for a checkbox indicates True - that is, the box
has been checked, otherwise no value is sent to the server. In this case, False
has been set as a possible False value for the form to accept, for some testing
purposes, but for some purposes (eg in validation, error throwing checks), this
behaviour means it can be omitted, meaning less test cases.

"""
import flask
import pytest

from werkzeug.datastructures import ImmutableMultiDict

from illnesses import measles
from probable_immunity_web_app.illnesses import Measles

from tests.request_generator_helpers import flatten_dict


def test_immunity_measles(client, app_specific_illnesses):
    """Test response and redirect on good data."""
    request_data = {'birth_year': 1985,
                    'measles': {'on_time_measles_vaccinations': 1,
                                'measles_illness': False},
                    }

    app = app_specific_illnesses(illnesses=[Measles])
    with app.test_client() as test_client:
        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

    assert test_client.get('immunity/').status_code == 200

    response = test_client.post(
        'immunity/', data=flat_request_data)

    assert response.status_code == 302  # Redirected to results page.
    assert response.headers['Location'] == 'http://localhost/immunity/results/'


@pytest.mark.parametrize(
    'request_data, messages',
    [
        ({'birth_year': 2001,
          'measles': {'on_time_measles_vaccinations': ''},  # No data.
          },
         (b'Please enter the number of measles vaccinations by age six, if none, enter 0.',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'measles': {'on_time_measles_vaccinations': 'test text entry'},  # String.
          },
         (b'Number of measles vaccinations by age six must be an integer',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'measles': {'on_time_measles_vaccinations': None},  # Test None/non str or int entry.
          },
         (b'Please enter the number of measles vaccinations by age six',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'measles': {'on_time_measles_vaccinations': 1.5},  # Test float.
          },
         (b'Number of measles vaccinations by age six must be an integer',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'measles': {'on_time_measles_vaccinations': -2},  # Test negative.
          },
         (b'Number of measles vaccinations by age six must be an integer',
          b'Error',),
         ),
        # With measles_illness set:
        ({'birth_year': 2001,
          'measles': {'on_time_measles_vaccinations': '',
                      'measles_illness': True},  # No data.
          },
         (b'Please enter the number of measles vaccinations by age six, if none, enter 0.',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'measles': {'on_time_measles_vaccinations': 'test text entry',
                      'measles_illness': True},  # String.
          },
         (b'Number of measles vaccinations by age six must be an integer',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'measles': {'on_time_measles_vaccinations': None,
                      'measles_illness': True},  # Test None/non str or int entry.
          },
         (b'Please enter the number of measles vaccinations by age six',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'measles': {'on_time_measles_vaccinations': 1.5,
                      'measles_illness': True},  # Test float.
          },
         (b'Number of measles vaccinations by age six must be an integer',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'measles': {'on_time_measles_vaccinations': -2,
                      'measles_illness': True},  # Test negative.
          },
         (b'Number of measles vaccinations by age six must be an integer',
          b'Error',),
         ),
        pytest.param({'birth_year': 2001,
                      'measles': {'on_time_measles_vaccinations': 2},
                      },
                     (b'Error',),
                     marks=pytest.mark.xfail),  # Integer should not error.
        pytest.param({'birth_year': 2001,
                      'measles': {'on_time_measles_vaccinations': 0},
                      },
                     (b'Birth year must be a 4 digit integer less than',
                      b'Error',),
                     marks=pytest.mark.xfail),  # Zero should not error.
        # measles_illness_errors: Difficult to send invalid data:
        # Generally, any value submitted for a checkbox indicates True - that
        # is, box has been checked, otherwise no value is sent to the server.
        # In this case, False has been set as a possible False value for the
        # form to accept, for testing purposes.

        # Test multiple errors:
        ({'birth_year': 'test text entry for both',
          'measles': {'on_time_measles_vaccinations': 'and both errors flashed'},
          },
         (b'Birth year must be a 4 digit integer less than',
          b'Number of measles vaccinations by age six must be an integer',
          b'Error',
          ),
         ),
    ])
def test_immunity_validate_measles_input(client, app_specific_illnesses,
                                         request_data,
                                         messages):
    app = app_specific_illnesses(illnesses=[Measles])
    with app.test_client() as test_client:
        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

    assert test_client.get('immunity/').status_code == 200

    response = test_client.post(
        'immunity/', data=flat_request_data)

    for error in messages:
        assert error in response.data


@pytest.mark.parametrize(
    'request_data',
    [  # 0 shots
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': False},
          }),
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': False},
          }),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': False},
          }),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': False},
          }),
        # 1 shot
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 1,
                      'measles_illness': False},
          }),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 1,
                      'measles_illness': False},
          }),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 1,
                      'measles_illness': False},
          }),
        # 2 shots
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 2,
                      'measles_illness': False},
          }),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 2,
                      'measles_illness': False},
          }),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 2,
                      'measles_illness': False},
          }),
        # >2 shots
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 3,
                      'measles_illness': False},
          }),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 7,
                      'measles_illness': False},
          }),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 12,
                      'measles_illness': False},
          }),
        # Measles illness True
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': True}
          }),
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': True}
          }),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': True}
          }),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': True}
          }),
        # 1 shot
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 1,
                      'measles_illness': True}
          }),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 1,
                      'measles_illness': True}
          }),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 1,
                      'measles_illness': True}
          }),
        # 2 shots
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 2,
                      'measles_illness': True}
          }),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 2,
                      'measles_illness': True}
          }),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 2,
                      'measles_illness': True}
          }),
        # >2 shots
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 3,
                      'measles_illness': True}
          }),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 7,
                      'measles_illness': True}
          }),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 12,
                      'measles_illness': True}
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
            'on_time_measles_vaccinations': int(request_data['measles']['on_time_measles_vaccinations']),
            'measles_illness': request_data['measles']['measles_illness'],
        }

        # Ensure successful redirect to results in response.
        assert 'http://localhost/immunity/results/' == response.headers['Location']


@pytest.mark.parametrize(
    'request_data, response_status, measles_probability',
    # Combinations years: 1956/1957/1958/1985/2011, measles shots: 0,1,2,many
    [  # 0 measles shots.
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': 0},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 0},
          },
         200, measles.shots_under_6_immunity[0]),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 0},
          },
         200, measles.shots_under_6_immunity[0]),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 0},
          },
         200, measles.shots_under_6_immunity[0]),
        # 1 measles shot.
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': 1},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 1},
          },
         200, measles.shots_under_6_immunity[1]),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 1},
          },
         200, measles.shots_under_6_immunity[1]),
        ({'birth_year': 1985,
          'measles': {'on_time_measles_vaccinations': 1},
          },
         200, measles.shots_under_6_immunity[1]),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 1},
          },
         200, measles.shots_under_6_immunity[1]),
        # 2 measles shots
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': 2},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 2},
          },
         200, measles.shots_under_6_immunity[2]),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 2},
          },
         200, measles.shots_under_6_immunity[2]),
        ({'birth_year': 1985,
          'measles': {'on_time_measles_vaccinations': 2},
          },
         200, measles.shots_under_6_immunity[2]),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 2},
          },
         200, measles.shots_under_6_immunity[2]),
        # >2 shots
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': 3},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 12},
          },
         200, measles.shots_under_6_immunity[2]),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 3},
          },
         200, measles.shots_under_6_immunity[2]),
        ({'birth_year': 1985,
          'measles': {'on_time_measles_vaccinations': 7},
          },
         200, measles.shots_under_6_immunity[2]),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 12},
          },
         200, measles.shots_under_6_immunity[2]),
        # measles_illness: True
        # 0 measles shots.
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 0,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        # 1 measles shot.
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': 1,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 1,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 1,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1985,
          'measles': {'on_time_measles_vaccinations': 1,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 1,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        # 2 measles shots
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': 2,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 2,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 2,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1985,
          'measles': {'on_time_measles_vaccinations': 2,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 2,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        # >2 shots
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': 3,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 12,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 3,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1985,
          'measles': {'on_time_measles_vaccinations': 7,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 12,
                      'measles_illness': True},
          },
         200, measles.conferred_immunity),
    ])
def test_measles_immunity_results(client, app_specific_illnesses,
                                  request_data,
                                  response_status, measles_probability):
    """Test all normally active components. Use range of normal values and edge cases."""
    app = app_specific_illnesses(illnesses=[Measles])
    with app.test_client() as test_client:
        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

        assert test_client.get('immunity/').status_code == 200
        response = test_client.post(
            'immunity/', data=flat_request_data)
        assert 'http://localhost/immunity/results/' == response.headers['Location']

        response = test_client.get('http://localhost/immunity/results/', follow_redirects=True)
        assert response.status_code == response_status
        # Use probability of measles immunity to test response content.
        assert f'{measles_probability:.2f}'.encode('utf-8') in response.data


@pytest.mark.parametrize(
    'session_data',
    [({'birth_year': 1980, 'on_time_measles_vaccinations': 2.5}),  # Float measles shots value.
     ({'birth_year': 1980, 'on_time_measles_vaccinations': 'Two'}),  # String measles shots value.
     ({'birth_year': 1980, 'on_time_measles_vaccinations': -1}),  # Negative measles shots value.
     # Missing or null measles shots value interpreted by algorithm as no shots.
     pytest.param({'birth_year': 1980, },
                  marks=pytest.mark.xfail),  # Missing measles shots value  interpreted as 0 shots.
     pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': ''},
                  marks=pytest.mark.xfail),  # Empty measles shots value evaluates False and interpreted as 0 shots.
     pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': None},
                  marks=pytest.mark.xfail),  # None measles shots value and interpreted as 0 shots.
     # Ensure good session data does not raise error.
     pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 2}, marks=pytest.mark.xfail),
     ])
def test_immunity_results_raising_error_measles(client, app_specific_illnesses,
                                                session_data):
    app = app_specific_illnesses(illnesses=[Measles])
    with app.test_client() as test_client:
        assert test_client.get('immunity/').status_code == 200

        # Fake out session data (ie in case a session is faked).
        with test_client.session_transaction() as test_client_session:
            test_client_session['birth_year'] = session_data['birth_year']
            try:
                test_client_session['measles'] = {
                    'on_time_measles_vaccinations': session_data['on_time_measles_vaccinations']}
            except KeyError:
                pass  # Case where no key in session dict for measles shots.

        response = test_client.get('http://localhost/immunity/results/', follow_redirects=True)

        assert b'An error was encountered.' in response.data


def test_immunity_results_without_session_data_redirects(client, app_specific_illnesses):
    app = app_specific_illnesses(illnesses=[Measles])
    with app.test_client() as test_client:
        assert test_client.get('immunity/').status_code == 200
        with test_client.session_transaction() as test_client_session:
            # Assert data not in session:
            with pytest.raises(KeyError):
                assert test_client_session['birth_year']
            with pytest.raises(KeyError):
                assert test_client_session['measles']['on_time_measles_vaccinations']
        response = test_client.get('immunity/results/', follow_redirects=False)
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/immunity/'


def test_immunity_results_without_valid_session_redirects_to_data_entry(client, app_specific_illnesses):
    app = app_specific_illnesses(illnesses=[Measles])
    with app.test_client() as test_client:
        assert test_client.get('immunity/').status_code == 200
        with test_client.session_transaction() as test_client_session:
            # Assert data not in session:
            with pytest.raises(KeyError):
                assert test_client_session['birth_year']
            with pytest.raises(KeyError):
                assert test_client_session['measles']['on_time_measles_vaccinations']

        response = test_client.get('immunity/results/', follow_redirects=True)
        assert response.status_code == 200
