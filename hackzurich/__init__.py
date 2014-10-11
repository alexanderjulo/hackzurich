from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from .config import get_config


def create_app(configObject=False):
    app = Flask(__name__)

    if configObject:
        app.config.from_object(configObject)
    else:
        app.config.from_object(get_config(app))

    db.init_app(app)

    import api
    api.setUp(app)

    return app


db = SQLAlchemy()
