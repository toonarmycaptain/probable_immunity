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




# def test_measles_immunity_results(client, app):
#     assert client.post('immunity_app/measles_immunity/results').status_code == 200
#     response = client.post(
#         'immunity_app/measles_immunity', data={'birth_year': '2019',
#                                                'on_time_measles_vaccinations': '1'}
#     )
#     assert 'http://localhost/immunity_app/measles_immunity/results' == response.headers['Location']
