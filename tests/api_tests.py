from . import BaseTestCase


class APITestCase(BaseTestCase):

    def test_json(self):
        """
            Assert that inexistent products won't be found
        """
        r = self.client.get("/api/1234567890123/")
        assert r.status_code == 404
