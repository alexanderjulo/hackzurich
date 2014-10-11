from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


def create_app(configObject=False):
    app = Flask(__name__)

    if configObject:
        app.config.from_object(configObject)

    db.init_app(app)

    return app


db = SQLAlchemy()
