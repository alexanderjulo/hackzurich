from flask import jsonify
from flask.ext.classy import FlaskView
from .models import Product
from .translate import translate


class APIView(FlaskView):
    """
        All recipes can be retrieved using the API. The api is available
        below `/api/`.

        Currently there is only one endpoint and one supported method.
    """

    def get(self, ean):
        product = Product.query.filter(
            Product.ean == ean
        ).first()
        if not product:
            return jsonify({
                'error': 'A product with this EAN could not be found.'
                }), 404
        # TODO: search recipe database for data
        english = translate(product.name)

        return jsonify({
            'name': english,
            'recipes': [
            ]
        })


def setUp(app):
    APIView.register(app)
