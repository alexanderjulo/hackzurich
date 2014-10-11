import requests
from . import db
from .models import Category, Product


def crawl_category(category_json, parent_id=None):
    category = Category.query.filter(
        Category.migros_id == category_json['id']
    ).first()
    if not category:
        category = Category()
        category.migros_id = category_json['id']
        category.name = category_json['name'][:99]
        category.description = category_json.get('description')[:99]
        category.parent_category_id = parent_id
        db.session.add(category)
        db.session.commit()
    if category_json.get('catMbrs'):
        for subcategory_json in category_json.get('catMbrs'):
            crawl_category(subcategory_json, parent_id=category.id)


def crawl():
    categories = requests.get("http://api.autoidlabs.ch/categories").json()
    crawl_category(categories)

    categories = Category.query.all()
    for category in categories:
        category_json = requests.get("http://api.autoidlabs.ch/categories/%s" %
                                     category.migros_id).json()
        if category_json.get("prodMbrs"):
            for product_json in category_json.get("prodMbrs"):
                product = Product.query.filter(
                    Product.migros_id == product_json.get("id")
                ).first()
                if not product:
                    product = Product()
                    product.name = product_json.get("name")[:99]
                    product.ean = product_json.get("ean")
                    product.migros_id = product_json.get("id")
                    product.subtitle = product_json.get("subtit")[:99]
                    product.category_id = category.id
                    db.session.add(product)
                    db.session.commit()
