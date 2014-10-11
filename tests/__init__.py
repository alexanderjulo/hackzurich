from flask.ext.testing import TestCase
from factory.alchemy import SQLAlchemyModelFactory
from hackzurich import create_app, db


class BaseFactory(SQLAlchemyModelFactory):
    FACTORY_SESSION = db.session


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
