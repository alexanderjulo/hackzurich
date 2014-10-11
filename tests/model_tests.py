from factory import SubFactory
from hackzurich.models import Category, Product
from . import BaseFactory


class CategoryFactory(BaseFactory):
    FACTORY_FOR = Category

    name = "Lebensmittel"
    description = "anything you could possibly eat"
    migros_id = "1234567"


class ProductFactory(BaseFactory):
    FACTORY_FOR = Product

    name = "Speck"
    subtitle = "mhhhmmm tasty..."
    migros_id = "123456789"
    ean = "2254623003971"
    category = SubFactory(CategoryFactory)
