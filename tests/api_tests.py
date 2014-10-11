from hackzurich import db
from . import BaseTestCase
from .model_tests import ProductFactory


class APITestCase(BaseTestCase):

    def test_json(self):
        """
            Assert that inexistent products won't be found
        """
        r = self.client.get("/api/1234567890123")
        assert r.status_code == 404

    def test_bacon(self):
        """
            Verify that the bacon can be found
        """
        bacon = ProductFactory()
        db.session.flush()
        r = self.client.get('/api/2254623003971')
        assert r.status_code == 200
        assert r.json is not None
        assert r.json['product']['id'] == bacon.id
        recipes = r.json.get('recipes')
        assert recipes is not None and len(recipes) == 0

    def test_bacon_recipes(self):
        """
            Verify that recipe retrieval works
        """
        ProductFactory()
        db.session.flush()
        r = self.client.get('/api/2254623003971?recipes=1')
        assert r.status_code == 200
        recipes = r.json.get('recipes')
        assert recipes is not None and len(recipes) > 0
