import json
from flask import jsonify, request
from flask.ext.classy import FlaskView
from .models import Product, RecipeCache
from .translate import translate
from . import yummly, db


def add_cors_support(response):
    """
        Allows cross domain requests for all domains, with all requested
        headers if necessary.
    """
    # I would use *, but I can't because then credentials don't work.
    response.headers['Access-Control-Allow-Origin'] = \
        request.headers.get('Origin')
    if request.headers.get('Access-Control-Request-Headers'):
        response.headers['Access-Control-Allow-Headers'] = \
            request.headers['Access-Control-Request-Headers']
    # allow credentials
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = \
        'POST, GET, PUT, PATCH, DELETE, OPTIONS'
    return response


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

        if request.args.get("recipes") and request.args.get("recipes") == '1':
            recipes = RecipeCache.query.filter(
                RecipeCache.product_id == product.id
            ).all()
            if not recipes:
                recipes = yummly.search(english)['matches']
                for recipe in recipes:
                    cache = RecipeCache()
                    cache.product_id = product.id
                    cache.yummly_id = recipe['id'][:30]
                    cache.json = json.dumps(recipe)
                    db.session.add(cache)
                db.session.commit()
                recipes = RecipeCache.query.filter(
                    RecipeCache.product_id == product.id
                ).all()
        else:
            recipes = []

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
                'id': product.category_id,
                'name': product.category.name,
                'description': product.category.name,
                'migros_id': product.category.migros_id,
                'parent_id': product.category.parent_category_id
            }

        for recipe in recipes:
            recipe_json = json.loads(recipe.json)
            response['recipes'].append({
                'rating': recipe_json['rating'],
                'time': recipe_json['totalTimeInSeconds'],
                'ingredients': recipe_json['ingredients'],
                'smallImageUrls': recipe_json['smallImageUrls'],
                'name': recipe_json['recipeName'],
                'id': recipe_json['id']
            })

        return jsonify(response), 200


def setUp(app):
    APIView.register(app)
    app.after_request(add_cors_support)
