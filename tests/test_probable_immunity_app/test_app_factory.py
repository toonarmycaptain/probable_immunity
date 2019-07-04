from pathlib import Path

import flask

import probable_immunity_web_app.app_factory as app_factory

from probable_immunity_web_app.app_factory import about_text_string, create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_about_text(client):
    response = client.get('/about_text')
    assert response.data == about_text_string


def test_create_app():
    app = create_app()
    assert isinstance(app, flask.app.Flask)
    assert app.name == 'probable_immunity_web_app.app_factory'


def test_create_app_passing_os_error(monkeypatch):
    def mocked_mkdir(app_instance_path, parents, exist_ok):
        if not isinstance(app_instance_path, Path) and parents is True and exist_ok is True:
            raise ValueError
        raise OSError

    monkeypatch.setattr(app_factory.Path, 'mkdir', mocked_mkdir)

    assert create_app()
