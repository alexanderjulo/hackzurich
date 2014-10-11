from flask.ext.testing import TestCase
from hackzurich import create_app, db


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app()
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
