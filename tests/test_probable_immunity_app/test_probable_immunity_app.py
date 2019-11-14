import flask
import pytest

from werkzeug.datastructures import ImmutableMultiDict

from illnesses import measles
from probable_immunity_web_app.illnesses import Measles
from probable_immunity_web_app.forms.immunity_data_entry_form import current_year

from tests.request_generator_helpers import flatten_dict


def test_immunity_common_data(client, app_specific_illnesses):
    """Test response and redirect on good data."""
    request_data = {'birth_year': 2019, }

    app = app_specific_illnesses(illnesses=[])
    with app.test_client() as test_client:
        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

    assert test_client.get('immunity/').status_code == 200

    response = test_client.post(
        'immunity/', data=flat_request_data)

    assert response.status_code == 302  # Redirected to results page.
    assert response.headers['Location'] == 'http://localhost/immunity/results/'


def test_immunity_all_good_data(client, app):
    """Test response and redirect on good data."""
    request_data = {'birth_year': 1985,
                    'measles': {'on_time_measles_vaccinations': 1},
                    'mumps': {'on_time_mumps_vaccinations': 2,
                              'mumps_illness': False},
                    }

    with client as test_client:
        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

    assert test_client.get('immunity/').status_code == 200

    response = test_client.post(
        'immunity/', data=flat_request_data)

    assert response.status_code == 302  # Redirected to results page.
    assert response.headers['Location'] == 'http://localhost/immunity/results/'


def test_immunity_without_trailing_forward_slash_redirects(client, app):
    response = client.get('immunity')
    assert response.status_code == 308
    assert response.headers['Location'] == 'http://localhost/immunity/'


@pytest.mark.parametrize(
    'request_data, messages',
    [
        ({'birth_year': '', },  # Test no entry.
         (b'Birth year required.',
          b'Error',),
         ),
        ({'birth_year': None, },  # Test None/non str or int entry.
         (b'Birth year required.',
          b'Error',),
         ),
        ({'birth_year': 1992.3, },  # Test float.
         (b'Not a valid integer value',
          b'Error',),
         ),
        ({'birth_year': 'test text entry', },  # Test str
         (b'Birth year must be a 4 digit integer less than',
          b'Error',),
         ),
        # Bounding:
        ({'birth_year': -1999, },  # Negative year should fail.
         (b'Birth year must be a 4 digit integer less than',
          b'Error',),
         ),
        ({'birth_year': 201, },  # > 4 digit year should fail.
         (b'Birth year must be a 4 digit integer less than',
          b'Error',),
         ),
        ({'birth_year': 19963, },  # > 4 digit year should fail.
         (b'Birth year must be a 4 digit integer less than',
          b'Error',),
         ),
        ({'birth_year': current_year + 1, },  # Next year should fail
         (b'Birth year must be a 4 digit integer less than',
          b'Error',),
         ),
        ({'birth_year': 3242, },  # Far future should fail.
         (b'Birth year must be a 4 digit integer less than',
          b'Error',),
         ),
        pytest.param({'birth_year': '1980', }, (b'Birth year must be a 4 digit integer less than',
                                                b'Error',),
                     marks=pytest.mark.xfail),  # Str convert to int is accepted.
        pytest.param({'birth_year': 1980, }, (b'Birth year must be a 4 digit integer less than',
                                              b'Error',),
                     marks=pytest.mark.xfail),  # Int is accepted without error.
    ])
def test_immunity_validate_common_data_input(client, app_specific_illnesses,
                                             request_data,
                                             messages):
    """Validate birth year, shared data."""
    app = app_specific_illnesses(illnesses=[])
    with app.test_client() as test_client:
        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

        assert test_client.get('immunity/').status_code == 200

        response = test_client.post(
            'immunity/', data=flat_request_data)
        for error in messages:
            assert error in response.data


@pytest.mark.parametrize(
    'request_data',
    [  # Strings
        ({'birth_year': '1956',  # Pre-1957.
          }),
        ({'birth_year': '1957',
          }),
        ({'birth_year': '1958',  # Close post-1957.
          }),
        ({'birth_year': '1980',  # More recent.
          }),
        ({'birth_year': '2019',  # This year.
          }),
        # Integers
        ({'birth_year': '1956',  # Pre-1957.
          }),
        ({'birth_year': '1957',
          }),
        ({'birth_year': '1958',  # Close post-1957.
          }),
        ({'birth_year': '1980',  # More recent.
          }),
        ({'birth_year': '2019',  # This year.
          }),
        pytest.param({'birth_year': '', },
                     marks=pytest.mark.xfail),  # Empty str errors.
        pytest.param({'birth_year': 'Two thousand.', },
                     marks=pytest.mark.xfail),  # String errors.
        pytest.param({'birth_year': None, },
                     marks=pytest.mark.xfail),  # None errors.
        pytest.param({'birth_year': -199, },
                     marks=pytest.mark.xfail),  # Negative errors.
        pytest.param({'birth_year': 1980.5, },
                     marks=pytest.mark.xfail),  # Float errors.
    ])
def test_immunity_session_contents_common_data(client, app_specific_illnesses,
                                               request_data):
    app = app_specific_illnesses(illnesses=[])
    with app.test_client() as test_client:
        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

        assert test_client.get('immunity/').status_code == 200

        response = test_client.post(
            'immunity/', data=flat_request_data, content_type='application/x-www-form-urlencoded')

        assert flask.session['birth_year'] == int(request_data['birth_year'])

        # Ensure successful redirect to results in response.
        assert 'http://localhost/immunity/results/' == response.headers['Location']


@pytest.mark.parametrize(
    'request_data',
    [  # Strings
        ({'birth_year': '1956',  # Pre-1957.
          }),
        ({'birth_year': '1957',
          }),
        ({'birth_year': '1958',  # Close post-1957.
          }),
        ({'birth_year': '1980',  # More recent.
          }),
        ({'birth_year': '2019',  # This year.
          }),
        # Integers
        ({'birth_year': 1956,  # Pre-1957.
          }),
        ({'birth_year': 1957,
          }),
        ({'birth_year': 1958,  # Close post-1957.
          }),
        ({'birth_year': 1980,  # More recent.
          }),
        ({'birth_year': 2019,  # This year.
          }),
        pytest.param({'birth_year': '', },
                     marks=pytest.mark.xfail),  # Empty str errors.
        pytest.param({'birth_year': 'Two thousand.', },
                     marks=pytest.mark.xfail),  # String errors.
        pytest.param({'birth_year': None, },
                     marks=pytest.mark.xfail),  # None errors.
        pytest.param({'birth_year': -199, },
                     marks=pytest.mark.xfail),  # Negative errors.
        pytest.param({'birth_year': 1980.5, },
                     marks=pytest.mark.xfail),  # Float errors.
    ])
def test_immunity_session_contents_all_data(client, app_specific_illnesses,
                                            request_data):
    app = app_specific_illnesses(illnesses=[])
    with app.test_client() as test_client:
        flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

        assert test_client.get('immunity/').status_code == 200

        response = test_client.post(
            'immunity/', data=flat_request_data, content_type='application/x-www-form-urlencoded')

        assert flask.session['birth_year'] == int(request_data['birth_year'])

        # Ensure successful redirect to results in response.
        assert 'http://localhost/immunity/results/' == response.headers['Location']


@pytest.mark.parametrize(
    'request_data, response_status, measles_probability',
    [  # Varied years 0 measles, 2 mumps, mumps False, 2 rubella, rubella False,
        ({'birth_year': 1956,
          'measles': {'on_time_measles_vaccinations': 0},
          'mumps': {'on_time_mumps_vaccinations': 2, 'mumps_illness': False, },
          'rubella': {'rubella_vaccinations': 2, 'rubella_illness': False, },
          },
         200, measles.conferred_immunity),
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 0},
          'mumps': {'on_time_mumps_vaccinations': 2, 'mumps_illness': False, },
          'rubella': {'rubella_vaccinations': 2, 'rubella_illness': False, },
          },
         200, measles.shots_under_6_immunity[0]),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 0},
          'mumps': {'on_time_mumps_vaccinations': 2, 'mumps_illness': False, },
          'rubella': {'rubella_vaccinations': 2, 'rubella_illness': False, },
          },
         200, measles.shots_under_6_immunity[0]),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 0},
          'mumps': {'on_time_mumps_vaccinations': 2, 'mumps_illness': False, },
          'rubella': {'rubella_vaccinations': 2, 'rubella_illness': False, },
          },
         200, measles.shots_under_6_immunity[0]),
        # 1 measles, Varied mumps, 1 rubella, rubella False.
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 1},
          'mumps': {'on_time_mumps_vaccinations': 0, 'mumps_illness': False, },
          'rubella': {'rubella_vaccinations': 1, 'rubella_illness': False, },
          },
         200, measles.shots_under_6_immunity[1]),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 1},
          'mumps': {'on_time_mumps_vaccinations': 1, 'mumps_illness': True, },
          'rubella': {'rubella_vaccinations': 1, 'rubella_illness': False, },
          },
         200, measles.shots_under_6_immunity[1]),
        # 2 measles, varied mumps, 1 rubella, rubella True.
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 2},
          'mumps': {'on_time_mumps_vaccinations': 2, 'mumps_illness': False, },
          'rubella': {'rubella_vaccinations': 1, 'rubella_illness': True, },
          },
         200, measles.shots_under_6_immunity[2]),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 2},
          'mumps': {'on_time_mumps_vaccinations': 0, 'mumps_illness': True, },
          'rubella': {'rubella_vaccinations': 1, 'rubella_illness': True, },
          },
         200, measles.shots_under_6_immunity[2]),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 2},
          'mumps': {'on_time_mumps_vaccinations': 2, 'mumps_illness': True, },
          'rubella': {'rubella_vaccinations': 1, 'rubella_illness': True, },
          },
         200, measles.shots_under_6_immunity[2]),
        # 2 measles, 2 mumps, varied rubella.
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 2},
          'mumps': {'on_time_mumps_vaccinations': 2, 'mumps_illness': False, },
          'rubella': {'rubella_vaccinations': 0, 'rubella_illness': False, },
          },
         200, measles.shots_under_6_immunity[2]),
        ({'birth_year': 1958,
          'measles': {'on_time_measles_vaccinations': 2},
          'mumps': {'on_time_mumps_vaccinations': 2, 'mumps_illness': False, },
          'rubella': {'rubella_vaccinations': 1, 'rubella_illness': True, },
          },
         200, measles.shots_under_6_immunity[2]),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 2},
          'mumps': {'on_time_mumps_vaccinations': 2, 'mumps_illness': True, },
          'rubella': {'rubella_vaccinations': 2, 'rubella_illness': False, },
          },
         200, measles.shots_under_6_immunity[2]),
        # >2 shots
        ({'birth_year': 1957,
          'measles': {'on_time_measles_vaccinations': 3},
          'mumps': {'on_time_mumps_vaccinations': 2, 'mumps_illness': False, },
          'rubella': {'rubella_vaccinations': 0, 'rubella_illness': True, },
          },
         200, measles.shots_under_6_immunity[2]),
        ({'birth_year': 2011,
          'measles': {'on_time_measles_vaccinations': 12},
          'mumps': {'on_time_mumps_vaccinations': 12, 'mumps_illness': True, },
          'rubella': {'rubella_vaccinations': 1, 'rubella_illness': False, },
          },
         200, measles.shots_under_6_immunity[2]),
    ])
def test_immunity_results(client, app,
                          request_data,
                          response_status, measles_probability):
    """Test all normally active components. Use range of normal values and edge cases."""

    flat_request_data = ImmutableMultiDict(flatten_dict(request_data))

    assert client.get('immunity/').status_code == 200
    response = client.post(
        'immunity/', data=flat_request_data)
    assert 'http://localhost/immunity/results/' == response.headers['Location']

    response = client.get('http://localhost/immunity/results/', follow_redirects=True)
    assert response.status_code == response_status
    # Use probability of measles immunity to test response content.
    assert f'{measles_probability}'.encode('utf-8') in response.data


@pytest.mark.parametrize(
    'session_data',
    [  # NB Birth year not evaluated singly, so will not raise error. Will likely raise error in immunity functions.
        pytest.param({'birth_year': 'a', }, marks=pytest.mark.xfail),  # String birth_year.
        pytest.param({'birth_year': 1957.6, }, marks=pytest.mark.xfail),  # String on_time_measles_vaccinations.
        pytest.param({'birth_year': 'c', }, marks=pytest.mark.xfail),  # String for all values.
        # Ensure good session data does not raise error.
        pytest.param({'birth_year': 1980, }, marks=pytest.mark.xfail),
    ])
def test_immunity_results_raising_error_common_data(client, app_specific_illnesses,
                                                    session_data):
    app = app_specific_illnesses(illnesses=[])
    with app.test_client() as test_client:
        assert test_client.get('immunity/').status_code == 200

        # Fake out session data (ie in case a session is faked).
        with test_client.session_transaction() as test_client_session:
            test_client_session['birth_year'] = session_data['birth_year']

        response = test_client.get('http://localhost/immunity/results/', follow_redirects=True)

        assert b'An error was encountered.' in response.data


@pytest.mark.parametrize(
    'session_data',
    [  # NB Test birth year raising error in measles algorithm.
        {'birth_year': 'a', },  # String birth_year.
        {'birth_year': 1957.6, },  # String on_time_measles_vaccinations.
        {'birth_year': 'c', },  # String for all values.
        {'birth_year': -1989, },  # Negative birth year
        {'birth_year': 2232},  # Too high birth year.
        {'birth_year': 19894, },  # Too long/high birth year.
        {'birth_year': 198, },  # Too low/short birth year.
        # Ensure good session data does not raise error.
        pytest.param({'birth_year': 1980}, marks=pytest.mark.xfail),
    ])
def test_immunity_results_raising_error_birth_year_using_measles(client,
                                                                 app_specific_illnesses,
                                                                 session_data):
    app = app_specific_illnesses(illnesses=[Measles])
    with app.test_client() as test_client:
        assert test_client.get('immunity/').status_code == 200

        # Fake out session data (ie in case a session is faked).
        with test_client.session_transaction() as test_client_session:
            test_client_session['birth_year'] = session_data['birth_year']
            test_client_session['measles'] = {'on_time_measles_vaccinations': 2, }
        response = test_client.get('http://localhost/immunity/results/', follow_redirects=True)

        assert b'An error was encountered.' in response.data


def test_immunity_results_without_session_data_redirects(client, app_specific_illnesses):
    # Use Measles as birth_year not used without an illness.
    app = app_specific_illnesses(illnesses=[Measles])
    with app.test_client() as test_client:
        assert test_client.get('immunity/').status_code == 200
        with test_client.session_transaction() as test_client_session:
            # Assert data not in session:
            with pytest.raises(KeyError):
                assert test_client_session['birth_year']

        response = test_client.get('immunity/results/', follow_redirects=False)
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/immunity/'


def test_immunity_results_without_trailing_forward_slash_redirects(client, app):
    response = client.get('immunity/results')
    assert response.status_code == 308
    assert response.headers['Location'] == 'http://localhost/immunity/results/'


def test_immunity_results_without_valid_session_redirects_to_data_entry(client, app_specific_illnesses, ):
    app = app_specific_illnesses(illnesses=[])
    with app.test_client() as test_client:
        assert test_client.get('immunity/').status_code == 200
        with test_client.session_transaction() as test_client_session:
            # Assert data not in session:
            with pytest.raises(KeyError):
                assert test_client_session['birth_year']

        response = test_client.get('immunity/results/', follow_redirects=True)
        assert response.status_code == 200
