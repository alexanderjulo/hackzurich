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
        """
            Returns product, category and recipe information in the
            following format:

            {
                product: {
                    id: '<id>',
                    name: '<name>',
                    subtitle: '<subtitle>',
                    ean: '<ean>',
                    migros_id: '<migros_id>',
                    name_english: '<name_english>',
                    category: {
                        id: '<id>',
                        name: '<name>',
                        description: '<description>',
                        migros_id: '<migros_id>',
                        parent_id: '<parent_id>'
                    }
                },
                recipes: [
                ]
            }

            Currently recipe information will not be returned yet.
        """
        product = Product.query.filter(
            Product.ean == ean
        ).first()
        if not product:
            return jsonify({
                'error': 'A product with this EAN could not be found.'
                }), 404

        english = translate(product.name)

        # TODO: search recipe database for data

        response = {
            'product': {
                'id': product.id,
                'name': product.name,
                'subtitle': product.subtitle,
                'ean': product.ean,
                'migros_id': product.migros_id,
                'name_english': english
            },
            'recipes': [
            ]
        }

        if product.category:
            response['product']['category'] = {
                'name': product.category.name,
                'description': product.category.name,
                'migros_id': product.category.migros_id,
                'parent_id': product.category.parent_category_id
            }

        return jsonify(response), 200


def setUp(app):
    APIView.register(app)
