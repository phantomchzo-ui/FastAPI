from app.catalog.model import Catalog
from app.dao.base import BaseDAO


class CatalogDAO(BaseDAO):
    model = Catalog
