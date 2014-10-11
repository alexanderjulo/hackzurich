from hackzurich import db
from hackzurich.models import RecipeCache
from . import BaseTestCase
from .model_tests import ProductFactory, CategoryFactory


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
        assert isinstance(recipes, list) and len(recipes) == 0

    def test_bacon_recipes(self):
        """
            Verify that recipe retrieval works
        """
        bacon = ProductFactory()
        db.session.flush()
        r = self.client.get('/api/2254623003971?recipes=1')
        assert r.status_code == 200
        recipes = r.json.get('recipes')
        assert recipes is not None and len(recipes) > 0

        recipes = RecipeCache.query.filter(
            RecipeCache.product_id == bacon.id
        ).all()
        assert len(recipes) > 0

    def test_search(self):
        """
            Check search results are complete
        """
        bacon = ProductFactory()
        notbaconbutrelated = ProductFactory(
            name="banane",
            subtitle="In Specksaft gelagert"
        )
        notatallbacon = ProductFactory(name="lauch")
        baconcategory = CategoryFactory(name="speck")
        db.session.flush()
        inbaconcategory = ProductFactory(category=baconcategory)
        db.session.commit()

        r = self.client.get('/api/search/speck')
        print r.data
        print r.status_code
        assert r.status_code == 200
        assert r.json is not None
        products = r.json
        assert len(products) == 3
