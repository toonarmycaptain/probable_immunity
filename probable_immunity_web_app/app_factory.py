import os

from pathlib import Path

from flask import Flask

about_text_string = (
    # Primarily for testing, hence binary string.
    b'<html>'
    b'<p><a href="https://github.com/toonarmycaptain/probable_immunity/">probable_immunity</a> '
    b'packages statistical data from various sources into a tool that can be used to give an idea '
    b'of the chance that a given individual might be immune to a given illness, based on supplied '
    b'vaccination and age information.</p>'
    b'<p>It should not be confused with medical advice or '
    b'taken as accurate on an individual basis in any way. Please consult a qualified medical '
    b'authority for medical advice.</p>'
    b'<p>The project is also a learning testbed and demonstrator '
    b'for <a href="https://twitter.com/toonarmycaptain">toonarmycaptain</a>.</p>'
    b'</html>')


def create_app(test_config=None):
    # Create, configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(32),
        DATABASE=Path(Path(app.instance_path), 'probable_immunity_app.sqlite'),  # plan to use PostgreSQL
    )

    if test_config is None:
        # Load instance config when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load test config.
        app.config.from_mapping(test_config)

    try:
        Path.mkdir(Path(app.instance_path), parents=True, exist_ok=True)
    except OSError:
        pass

    from . import probable_immunity_app
    app.register_blueprint(probable_immunity_app.immunity_app_bp)

    @app.route('/about_text/')
    def about_text():
        return about_text_string

    return app
