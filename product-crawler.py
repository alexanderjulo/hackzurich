import requests
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# create base
Base = declarative_base()

# create engine
engine = sa.create_engine('sqlite:///products.sqlite')

# create session
Session = sessionmaker(bind=engine)
session = Session()


class Category(Base):
    __tablename__ = 'categories'
    id = sa.Column(sa.Integer, primary_key=True)
    migros_id = sa.Column(sa.Integer)
    name = sa.Column(sa.String(100))
    description = sa.Column(sa.Text)
    parent_category_id = sa.Column(sa.Integer, sa.ForeignKey('categories.id'))


class Product(Base):
    __tablename__ = 'products'
    id = sa.Column(sa.Integer, primary_key=True)
    category_id = sa.Column(sa.Integer, sa.ForeignKey('categories.id'))
    name = sa.Column(sa.String(100))
    migros_id = sa.Column(sa.Integer)
    ean = sa.Column(sa.String(13))
    subtitle = sa.Column(sa.String(100))


def crawl_category(category_json, parent_id=None):
    category = session.query(Category).filter(
        Category.migros_id == category_json['id']
    ).first()
    if not category:
        category = Category()
        category.migros_id = category_json['id']
        category.name = category_json['name']
        category.description = category_json.get('description')
        category.parent_category_id = parent_id
        session.add(category)
        session.flush()
    if category_json.get('catMbrs'):
        for subcategory_json in category_json.get('catMbrs'):
            crawl_category(subcategory_json, parent_id=category.id)


def crawl():
    categories = requests.get("http://api.autoidlabs.ch/categories").json()
    crawl_category(categories)

    session.commit()

    categories = session.query(Category).all()
    for category in categories:
        category_json = requests.get("http://api.autoidlabs.ch/categories/%s" %
                                     category.migros_id).json()
        if category_json.get("prodMbrs"):
            for product_json in category_json.get("prodMbrs"):
                product = session.query(Product).filter(
                    Product.migros_id == product_json.get("id")
                ).first()
                if not product:
                    product = Product()
                    product.name = product_json.get("name")
                    product.ean = product_json.get("ean")
                    product.migros_id = product_json.get("id")
                    product.subtitle = product_json.get("subtit")
                    product.category_id = category.id
                    session.add(product)
                    session.commit()


def run():
    crawl()


if __name__ == '__main__':
    # create missing tables
    Base.metadata.create_all(engine)

    run()
