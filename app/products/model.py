from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[int]
    description: Mapped[str] = mapped_column(String(255))
    catalog_id: Mapped[int] = mapped_column(ForeignKey('catalog.id'))
    product_images: Mapped[str] = mapped_column(String(50))
