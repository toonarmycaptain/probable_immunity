import pytest

from probable_immunity_web_app.app_factory import create_app
from probable_immunity_web_app.illnesses import Mumps, Measles


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'ILLNESS_LIST': [Measles, Mumps],
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def app_specific_illnesses():
    def _test_illnesses(illnesses):
        # Enables testing with different configs, as setattrs persist.
        from probable_immunity_web_app.forms import immunity_data_entry_form
        from importlib import reload; reload(immunity_data_entry_form)
        app = create_app({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'ILLNESS_LIST': illnesses,
        })
        return app

    return _test_illnesses
