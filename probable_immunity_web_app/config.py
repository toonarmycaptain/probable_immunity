import os

from probable_immunity_web_app.illnesses import (Measles,
                                                 Mumps,
                                                 Rubella,
                                                 )


class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = b'some-secret-to-be-overridden'

    FLASK_SECRET = SECRET_KEY


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    SECRET_KEY = os.urandom(32)
    # DATABASE = Path(Path(app.instance_path), 'probable_immunity_app.sqlite'),  # plan to use PostgreSQL

    ILLNESS_LIST = [
        Measles,
        Mumps,
        Rubella,
    ]
