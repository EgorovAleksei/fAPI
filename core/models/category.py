from typing import Any, TYPE_CHECKING

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, intpk

if TYPE_CHECKING:
    from .product import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[intpk]
    # wb_id: Mapped[int]
    parent: Mapped[int] = mapped_column(nullable=True, default=None)
    name: Mapped[str]
    seo: Mapped[str] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(nullable=True)
    shard: Mapped[str] = mapped_column(nullable=True)
    query: Mapped[str] = mapped_column(nullable=True)
    childs: Mapped[bool] = mapped_column(default=True)
    published: Mapped[bool] = mapped_column(default=True)
    sub_category: Mapped[list[dict[Any, Any]]] = mapped_column(
        type_=JSONB, nullable=True, default=None
    )
    filter_category: Mapped[bool] = mapped_column(default=True)
    lft: Mapped[int]
    rght: Mapped[int]
    tree_id: Mapped[int]
    level: Mapped[int]

    product: Mapped[list["Product"]] = relationship(
        back_populates="category_relationship"
    )
