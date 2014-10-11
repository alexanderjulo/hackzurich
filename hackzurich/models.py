from . import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    migros_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    parent_category = db.relationship("Category", uselist=False)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    name = db.Column(db.String(100))
    migros_id = db.Column(db.Integer)
    ean = db.Column(db.String(13))
    subtitle = db.Column(db.String(100))

    category = db.relationship("Category", uselist=False)


class RecipeCache(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    yummly_id = db.Column(db.String(30))
    json = db.Column(db.Text)
