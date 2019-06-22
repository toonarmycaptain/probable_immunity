from pathlib import Path

from flask import Flask


def create_app(test_config=None):
    # Create, configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
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

    return app
