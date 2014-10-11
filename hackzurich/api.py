from flask import jsonify
from flask.ext.classy import FlaskView
from .models import Product


class APIView(FlaskView):

    def get(self, ean):
        product = Product.query.filter(
            Product.ean == ean
        ).first()
        if not product:
            return jsonify({
                'error': 'A product with this EAN could not be found.'
                }), 404
        # TODO: search recipe database for data
        return jsonify({
            'recipes': [
            ]
        })


def setUp(app):
    APIView.register(app)
