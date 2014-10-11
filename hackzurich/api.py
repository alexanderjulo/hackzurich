import json
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from flask import jsonify, request, Response
from flask.ext.classy import FlaskView, route
from .models import Product, RecipeCache, Category
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
            URL: `/api/<ean>`

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

            Add the recipes=1 query parameter to enable the return
            of recipes that include the product.

            This function will use queried recipes if possible to
            reduce the load on the API of yummly.
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

    def search(self, term):
        """
            URL: `/api/search/<term>`

            Search for a term within product name, product subtitle,
            category name and category description.

            Will output all data as a json encoded list.
        """
        like = "%{0}%"
        category = aliased(Category)
        query = Product.query.join(category).filter(
            or_(
                Product.name.ilike(like.format(term)),
                Product.subtitle.ilike(like.format(term)),
                category.name.ilike(like.format(term)),
                category.description.ilike(like.format(term))
            )
        )

        products = query.all()

        response = []
        for product in products:
            response.append({
                'id': product.id,
                'name': product.name,
                'subtitle': product.subtitle,
                'ean': product.ean,
                'migros_id': product.migros_id,
            })
        return Response(
            json.dumps(response),
            mimetype="application/json"
        ), 200 if len(response) > 0 else 404


def setUp(app):
    APIView.register(app)
    app.after_request(add_cors_support)
