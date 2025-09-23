from sqladmin import ModelView

from app.catalog.model import Catalog
from app.products.model import Product
from app.users.models import User


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = 'Users'
    column_list = [c.name for c in User.__table__.c]


class ProductAdmin(ModelView, model=Product):
    name = "Product"
    name_plural = 'Products'
    column_list = [c.name for c in Product.__table__.c]

class CatalogAdmin(ModelView, model=Catalog):
    name = "Catalog"
    name_plural = "Catalog"
    column_list = [c.name for c in Catalog.__table__.c]