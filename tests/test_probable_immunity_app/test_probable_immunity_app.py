import flask
import pytest


def test_immunity(client, app):
    assert client.get('immunity').status_code == 200
    response = client.post(
        'immunity', data={'birth_year': '2019',
                          'on_time_measles_vaccinations': '1'}
    )

    assert response.status_code == 302  # Redirected to results page.
    assert 'http://localhost/immunity/results' == response.headers['Location']


@pytest.mark.parametrize(
    'birth_year, on_time_measles_vaccinations, message',
    [('', 'unimportant, untested', b'Birth year required.'),
     ('2019', '', b'Number of measles immunisations before age six needed, if none, enter 0.'),
     ('test text entry', 'unimportant, untested', b'Birth year must be a number.'),
     ('2019', 'test text entry', b'Number of vaccinations must be a number.'),
     ('test text entry for both', 'and both errors flashed',
      b'Birth year must be a number.\nNumber of vaccinations must be a number.')
     ])
def test_immunity_validate_input(client, app,
                                 birth_year, on_time_measles_vaccinations,
                                 message):
    response = client.post(
        '/immunity',
        data={'birth_year': birth_year, 'on_time_measles_vaccinations': on_time_measles_vaccinations}
    )
    assert message in response.data


@pytest.mark.parametrize(
    'request_data',
    [  # 0 shots
        ({'birth_year': '1956', 'on_time_measles_vaccinations': '0'}),
        ({'birth_year': '1957', 'on_time_measles_vaccinations': '0'}),
        ({'birth_year': '1958', 'on_time_measles_vaccinations': '0'}),
        ({'birth_year': '2011', 'on_time_measles_vaccinations': '0'}),
        # 1 shot
        ({'birth_year': '1957', 'on_time_measles_vaccinations': '1'}),
        ({'birth_year': '1958', 'on_time_measles_vaccinations': '1'}),
        ({'birth_year': '2011', 'on_time_measles_vaccinations': '1'}),
        # 2 shots
        ({'birth_year': '1957', 'on_time_measles_vaccinations': '2'}),
        ({'birth_year': '1958', 'on_time_measles_vaccinations': '2'}),
        ({'birth_year': '2011', 'on_time_measles_vaccinations': '2'}),
        # >2 shots
        ({'birth_year': '1957', 'on_time_measles_vaccinations': '3'}),
        ({'birth_year': '1958', 'on_time_measles_vaccinations': '7'}),
        ({'birth_year': '2011', 'on_time_measles_vaccinations': '12'}),
    ])
def test_immunity_session_contents(client, app,
                                   request_data):
    with app.test_client() as test_client:
        assert test_client.get('immunity').status_code == 200
        response = test_client.post(
            'immunity', data=request_data)
        assert flask.session['birth_year'] == int(request_data['birth_year'])
        assert flask.session['measles'] == {
            'on_time_measles_vaccinations': int(request_data['on_time_measles_vaccinations'])}

        # Ensure successful redirect to results in response.
        assert 'http://localhost/immunity/results' == response.headers['Location']


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
def test_immunity_results(client, app,
                          request_data,
                          response_status, probability):
    assert client.get('immunity').status_code == 200
    response = client.post(
        'immunity', data=request_data)
    assert 'http://localhost/immunity/results' == response.headers['Location']

    response = client.get('http://localhost/immunity/results', follow_redirects=True)
    assert response.status_code == response_status
    # Use probability of immunity to test response content.
    assert probability in response.data


@pytest.mark.parametrize(
    'session_data',
    [
        ({'birth_year': 'a', 'on_time_measles_vaccinations': 0}),  # String birth_year.
        ({'birth_year': 1957, 'on_time_measles_vaccinations': 'b'}),  # String on_time_measles_vaccinations.
        ({'birth_year': 'c', 'on_time_measles_vaccinations': 'd'}),  # String for all values.
        # Ensure good session data does not raise error.
        pytest.param({'birth_year': 1980, 'on_time_measles_vaccinations': 2}, marks=pytest.mark.xfail),
    ])
def test_immunity_results_raising_error(client, app,
                                        session_data):
    with app.test_client() as test_client:
        assert test_client.get('immunity').status_code == 200

        # Fake out session data (ie in case a session is faked).
        with test_client.session_transaction() as test_client_session:
            test_client_session['birth_year'] = session_data['birth_year']
            test_client_session['measles'] = {
                'on_time_measles_vaccinations': session_data['on_time_measles_vaccinations']}

        response = test_client.get('http://localhost/immunity/results', follow_redirects=True)

        assert b'An error was encountered.' in response.data


def test_immunity_results_without_valid_session_redirects(client, app):
    with app.test_client() as test_client:
        assert test_client.get('immunity').status_code == 200
        with test_client.session_transaction() as test_client_session:
            with pytest.raises(KeyError):
                assert test_client_session['birth_year']
            with pytest.raises(KeyError):
                assert test_client_session['measles']['on_time_measles_vaccinations']
        response = test_client.get('immunity/results', follow_redirects=False)
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/immunity'


def test_immunity_results_without_valid_session_redirects_to_data_entry(client, app):
    with app.test_client() as test_client:
        assert test_client.get('immunity').status_code == 200
        with test_client.session_transaction() as test_client_session:
            with pytest.raises(KeyError):
                assert test_client_session['birth_year']
            with pytest.raises(KeyError):
                assert test_client_session['measles']['on_time_measles_vaccinations']
        response = test_client.get('immunity/results', follow_redirects=True)
        assert response.status_code == 200
