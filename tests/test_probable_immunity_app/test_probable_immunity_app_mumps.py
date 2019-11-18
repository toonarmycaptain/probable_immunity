"""
Test immunity app mumps illness.


NB Since mumps_illness is a checkbox, it is difficult to send invalid data, and
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

import illnesses

from illnesses import mumps
from probable_immunity_web_app.illnesses import Mumps

from tests.request_generator_helpers import flatten_dict


def test_immunity_mumps(client, app_specific_illnesses):
    """Test response and redirect on good data."""
    request_data = {'birth_year': 1985,
                    'mumps': {'on_time_mumps_vaccinations': 1,
                              'mumps_illness': False,
                              },
                    }

    app = app_specific_illnesses(illnesses=[Mumps])
    with app.test_client() as test_client:
        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

    assert test_client.get('immunity/').status_code == 200

    response = test_client.post(
        'immunity/', data=flat_request_data)

    assert response.status_code == 302  # Redirected to results page.
    assert response.headers['Location'] == 'http://localhost/immunity/results/'


@pytest.mark.parametrize(
    'request_data, messages',
    [  # on_time_mumps_vaccinations errors
        # mumps_illness implicitly set to False
        ({'birth_year': 2001,
          'mumps': {'on_time_mumps_vaccinations': ''},  # No data.
          },
         (b'Please enter the number of mumps vaccinations by age six, if none, enter 0.',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'mumps': {'on_time_mumps_vaccinations': 'test text entry'},  # String.
          },
         (b'Number of mumps vaccinations by age six must be an integer',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'mumps': {'on_time_mumps_vaccinations': None},  # Test None/non str or int entry.
          },
         (b'Please enter the number of mumps vaccinations by age six',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'mumps': {'on_time_mumps_vaccinations': 1.5},  # Test float.
          },
         (b'Number of mumps vaccinations by age six must be an integer',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'mumps': {'on_time_mumps_vaccinations': -2},  # Test negative.
          },
         (b'Number of mumps vaccinations by age six must be an integer',
          b'Error',),
         ),
        # With mumps_illness set:
        ({'birth_year': 2001,
          'mumps': {'on_time_mumps_vaccinations': '',
                    'mumps_illness': True},  # No data.
          },
         (b'Please enter the number of mumps vaccinations by age six, if none, enter 0.',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'mumps': {'on_time_mumps_vaccinations': 'test text entry',
                    'mumps_illness': True},  # String.
          },
         (b'Number of mumps vaccinations by age six must be an integer',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'mumps': {'on_time_mumps_vaccinations': None,
                    'mumps_illness': True},  # Test None/non str or int entry.
          },
         (b'Please enter the number of mumps vaccinations by age six',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'mumps': {'on_time_mumps_vaccinations': 1.5,
                    'mumps_illness': True},  # Test float.
          },
         (b'Number of mumps vaccinations by age six must be an integer',
          b'Error',),
         ),
        ({'birth_year': 2001,
          'mumps': {'on_time_mumps_vaccinations': -2,
                    'mumps_illness': True},  # Test negative.
          },
         (b'Number of mumps vaccinations by age six must be an integer',
          b'Error',),
         ),
        pytest.param({'birth_year': 2001,
                      'mumps': {'on_time_mumps_vaccinations': 2,
                                'mumps_illness': True},
                      },
                     (b'Error',),
                     marks=pytest.mark.xfail),  # Integer should not error.
        pytest.param({'birth_year': 2001,
                      'mumps': {'on_time_mumps_vaccinations': 0,
                                'mumps_illness': True},
                      },
                     (b'Birth year must be a 4 digit integer less than',
                      b'Error',),
                     marks=pytest.mark.xfail),  # Zero should not error.
        # mumps_illness_errors: Difficult to send invalid data:
        # Generally, any value submitted for a checkbox indicates True - that
        # is, box has been checked, otherwise no value is sent to the server.
        # In this case, False has been set as a possible False value for the
        # form to accept, for testing purposes.

        # Test multiple errors:
        ({'birth_year': 'test text entry for both',
          'mumps': {'on_time_mumps_vaccinations': 'and both errors flashed'},
          },
         (b'Birth year must be a 4 digit integer less than',
          b'Number of mumps vaccinations by age six must be an integer',
          b'Error',
          ),
         ),
    ])
def test_immunity_validate_mumps_input(client, app_specific_illnesses,
                                       request_data,
                                       messages):
    app = app_specific_illnesses(illnesses=[Mumps])
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
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': False},
          }),
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': False},
          }),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': False},
          }),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': False},
          }),
        # 1 shot
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 1,
                    'mumps_illness': False},
          }),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 1,
                    'mumps_illness': False},
          }),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 1,
                    'mumps_illness': False},
          }),
        # 2 shots
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 2,
                    'mumps_illness': False},
          }),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 2,
                    'mumps_illness': False},
          }),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 2,
                    'mumps_illness': False},
          }),
        # >2 shots
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 3,
                    'mumps_illness': False},
          }),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 7,
                    'mumps_illness': False},
          }),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 12,
                    'mumps_illness': False},
          }),
        # Mumps illness True
        ({'birth_year': 1956,
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': True}
          }),
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': True}
          }),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': True}
          }),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': True}
          }),
        # 1 shot
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 1,
                    'mumps_illness': True}
          }),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 1,
                    'mumps_illness': True}
          }),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 1,
                    'mumps_illness': True}
          }),
        # 2 shots
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 2,
                    'mumps_illness': True}
          }),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 2,
                    'mumps_illness': True}
          }),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 2,
                    'mumps_illness': True}
          }),
        # >2 shots
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 3,
                    'mumps_illness': True}
          }),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 7,
                    'mumps_illness': True}
          }),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 12,
                    'mumps_illness': True}
          }),
    ])
def test_immunity_session_contents_mumps(app_specific_illnesses,
                                         request_data,
                                         monkeypatch):
    app = app_specific_illnesses(illnesses=[Mumps])
    with app.test_client() as test_client:
        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

        assert test_client.get('immunity/').status_code == 200

        response = test_client.post(
            'immunity/', data=flat_request_data)

        assert flask.session['birth_year'] == request_data['birth_year']
        assert flask.session['mumps'] == {
            'on_time_mumps_vaccinations': request_data['mumps']['on_time_mumps_vaccinations'],
            'mumps_illness': request_data['mumps']['mumps_illness']}

        # Ensure successful redirect to results in response.
        assert 'http://localhost/immunity/results/' == response.headers['Location']


@pytest.mark.parametrize(
    'request_data, response_status, mumps_probability',
    # Combinations years: 1956/1957/1958/1985/2011, mumps shots: 0,1,2,many, mumps_illness F/T
    [  # mumps_illness: implicit False
        # 0 mumps shots.
        ({'birth_year': 1956,
          'mumps': {'on_time_mumps_vaccinations': 0},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 0},
          },
         200, mumps.natural_immunity),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 0},
          },
         200, mumps.natural_immunity),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 0},
          },
         200, mumps.natural_immunity),
        # 1 mumps shot.
        ({'birth_year': 1956,
          'mumps': {'on_time_mumps_vaccinations': 1},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 1},
          },
         200, 1.00),  # 1.00 for one shot
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 1},
          },
         200, 1.00),  # 1.00 for one shot
        ({'birth_year': 1985,
          'mumps': {'on_time_mumps_vaccinations': 1},
          },
         200, 1.00),  # 1.00 for one shot
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 1},
          },
         200, 1.00),  # 1.00 for one shot
        # 2 mumps shots
        ({'birth_year': 1956,
          'mumps': {'on_time_mumps_vaccinations': 2},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 2},
          },
         200, 2.00),  # 2.00 for two shots
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 2},
          },
         200, 2.00),  # 2.00 for two shots
        ({'birth_year': 1985,
          'mumps': {'on_time_mumps_vaccinations': 2},
          },
         200, 2.00),  # 2.00 for two shots
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 2},
          },
         200, 2.00),  # 2.00 for two shots
        # >2 shots
        ({'birth_year': 1956,
          'mumps': {'on_time_mumps_vaccinations': 3},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 12},
          },
         200, 2.00),  # 2.00 for two shots
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 3},
          },
         200, 2.00),  # 2.00 for two shots
        ({'birth_year': 1985,
          'mumps': {'on_time_mumps_vaccinations': 7},
          },
         200, 2.00),  # 2.00 for two shots
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 12},
          },
         200, 2.00),  # 2.00 for two shots
        # mumps_illness: True
        # 0 mumps shots.
        ({'birth_year': 1956,
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 0,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        # 1 mumps shot.
        ({'birth_year': 1956,
          'mumps': {'on_time_mumps_vaccinations': 1,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 1,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 1,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1985,
          'mumps': {'on_time_mumps_vaccinations': 1,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 1,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        # 2 mumps shots
        ({'birth_year': 1956,
          'mumps': {'on_time_mumps_vaccinations': 2,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 2,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 2,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1985,
          'mumps': {'on_time_mumps_vaccinations': 2,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 2,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        # >2 shots
        ({'birth_year': 1956,
          'mumps': {'on_time_mumps_vaccinations': 3,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1957,
          'mumps': {'on_time_mumps_vaccinations': 12,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1958,
          'mumps': {'on_time_mumps_vaccinations': 3,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 1985,
          'mumps': {'on_time_mumps_vaccinations': 7,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),
        ({'birth_year': 2011,
          'mumps': {'on_time_mumps_vaccinations': 12,
                    'mumps_illness': True},
          },
         200, mumps.conferred_immunity),

    ])
def test_mumps_immunity_results(client, app_specific_illnesses, monkeypatch,
                                request_data,
                                response_status, mumps_probability):
    """Test all normally active components. Use range of normal values and edge cases."""

    def mocked_one_dose_immunity(*ignored_args):
        return 1.00  # 1.00 for one shot

    def mocked_two_dose_immunity(*ignored_args):
        return 2.00  # 2.00 for two shots

    monkeypatch.setattr(illnesses.mumps, 'one_dose_immunity', mocked_one_dose_immunity)
    monkeypatch.setattr(illnesses.mumps, 'two_dose_immunity', mocked_two_dose_immunity)

    app = app_specific_illnesses(illnesses=[Mumps])
    with app.test_client() as test_client:
        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

        assert test_client.get('immunity/').status_code == 200
        response = test_client.post(
            'immunity/', data=flat_request_data)
        assert 'http://localhost/immunity/results/' == response.headers['Location']

        response = test_client.get('http://localhost/immunity/results/', follow_redirects=True)
        assert response.status_code == response_status
        # Use probability of mumps immunity to test response content.
        assert f'{mumps_probability}'.encode('utf-8') in response.data


@pytest.mark.parametrize(
    'session_data',
    [({'birth_year': 1980, 'on_time_mumps_vaccinations': 2.5}),  # Float mumps shots value.
     ({'birth_year': 1980, 'on_time_mumps_vaccinations': 'Two'}),  # String mumps shots value.
     ({'birth_year': 1980, 'on_time_mumps_vaccinations': -1}),  # Negative mumps shots value.
     # Missing or null mumps shots value interpreted by algorithm as no shots.
     pytest.param({'birth_year': 1980, },
                  marks=pytest.mark.xfail),  # Missing mumps shots value  interpreted as 0 shots.
     pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': ''},
                  marks=pytest.mark.xfail),  # Empty mumps shots value evaluates False and interpreted as 0 shots.
     pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': None},
                  marks=pytest.mark.xfail),  # None mumps shots value and interpreted as 0 shots.
     # Ensure good session data does not raise error.
     pytest.param({'birth_year': 1980, 'on_time_mumps_vaccinations': 2}, marks=pytest.mark.xfail),
     ])
def test_immunity_results_raising_error_mumps(client, app_specific_illnesses,
                                              session_data):
    app = app_specific_illnesses(illnesses=[Mumps])
    with app.test_client() as test_client:
        assert test_client.get('immunity/').status_code == 200

        # Fake out session data (ie in case a session is faked).
        with test_client.session_transaction() as test_client_session:
            test_client_session['birth_year'] = session_data['birth_year']
            try:
                test_client_session['mumps'] = {
                    'on_time_mumps_vaccinations': session_data['on_time_mumps_vaccinations']}
            except KeyError:
                pass  # Case where no key in session dict for mumps shots.

        response = test_client.get('http://localhost/immunity/results/', follow_redirects=True)

        assert b'An error was encountered.' in response.data


def test_immunity_results_without_session_data_redirects(client, app_specific_illnesses):
    app = app_specific_illnesses(illnesses=[Mumps])
    with app.test_client() as test_client:
        assert test_client.get('immunity/').status_code == 200
        with test_client.session_transaction() as test_client_session:
            # Assert data not in session:
            with pytest.raises(KeyError):
                assert test_client_session['birth_year']
            with pytest.raises(KeyError):
                assert test_client_session['mumps']['on_time_mumps_vaccinations']
        response = test_client.get('immunity/results/', follow_redirects=False)
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/immunity/'


def test_immunity_results_without_valid_session_redirects_to_data_entry(client, app_specific_illnesses):
    app = app_specific_illnesses(illnesses=[Mumps])
    with app.test_client() as test_client:
        assert test_client.get('immunity/').status_code == 200
        with test_client.session_transaction() as test_client_session:
            # Assert data not in session:
            with pytest.raises(KeyError):
                assert test_client_session['birth_year']
            with pytest.raises(KeyError):
                assert test_client_session['mumps']['on_time_mumps_vaccinations']

        response = test_client.get('immunity/results/', follow_redirects=True)
        assert response.status_code == 200
