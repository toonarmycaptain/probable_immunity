import pytest


def test_measles_immunity(client, app):
    assert client.get('immunity_app/measles_immunity').status_code == 200
    response = client.post(
        'immunity_app/measles_immunity', data={'birth_year': '2019',
                                               'on_time_measles_vaccinations': '1'}
    )
    assert 'http://localhost/immunity_app/measles_immunity/results' == response.headers['Location']


@pytest.mark.parametrize(
    'birth_year, on_time_measles_vaccinations, message',
    [('', 'unimportant, untested', b'Birth year required.'),
     ('2019', '', b'Number of measles immunisations before age six needed, if none, enter 0.'),
     ('test text entry', 'unimportant, untested', b'Birth year must be a number.'),
     ('2019', 'test text entry', b'Number of vaccinations must be a number.'),
     ('test text entry for both', 'and both errors flashed',
      b'Birth year must be a number.\nNumber of vaccinations must be a number.')
     ])
def test_measles_immunity_validate_input(client, app,
                                         birth_year, on_time_measles_vaccinations,
                                         message):
    response = client.post(
        '/immunity_app/measles_immunity',
        data={'birth_year': birth_year, 'on_time_measles_vaccinations': on_time_measles_vaccinations}
    )
    assert message in response.data


@pytest.mark.parametrize(
    'request_data, response_status, probability',
    [  # 0 shots
        ({'birth_year': '1956', 'on_time_measles_vaccinations': '0'}, 200, b'1.0'),
        ({'birth_year': '1957', 'on_time_measles_vaccinations': '0'}, 200, b'0.0'),
        ({'birth_year': '1958', 'on_time_measles_vaccinations': '0'}, 200, b'0.0'),
        ({'birth_year': '2011', 'on_time_measles_vaccinations': '0'}, 200, b'0.0'),
        # 1 shot
        ({'birth_year': '1957', 'on_time_measles_vaccinations': '1'}, 200, b'0.93'),
        ({'birth_year': '1958', 'on_time_measles_vaccinations': '1'}, 200, b'0.93'),
        ({'birth_year': '2011', 'on_time_measles_vaccinations': '1'}, 200, b'0.93'),
        # 2 shots
        ({'birth_year': '1957', 'on_time_measles_vaccinations': '2'}, 200, b'0.97'),
        ({'birth_year': '1958', 'on_time_measles_vaccinations': '2'}, 200, b'0.97'),
        ({'birth_year': '2011', 'on_time_measles_vaccinations': '2'}, 200, b'0.97'),
        # >2 shots
        ({'birth_year': '1957', 'on_time_measles_vaccinations': '3'}, 200, b'0.97'),
        ({'birth_year': '1958', 'on_time_measles_vaccinations': '7'}, 200, b'0.97'),
        ({'birth_year': '2011', 'on_time_measles_vaccinations': '12'}, 200, b'0.97'),
    ])
def test_measles_immunity_results(client, app,
                                  request_data,
                                  response_status, probability):
    assert client.get('immunity_app/measles_immunity').status_code == 200
    response = client.post(
        'immunity_app/measles_immunity', data=request_data)
    assert 'http://localhost/immunity_app/measles_immunity/results' == response.headers['Location']

    response = client.get('http://localhost/immunity_app/measles_immunity/results', follow_redirects=True)
    assert response.status_code == response_status
    # Use probability of immunity to test response content.
    assert probability in response.data
