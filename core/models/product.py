from typing import Any, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, intpk

if TYPE_CHECKING:
    from .category import Category


class Product(Base):
    __tablename__ = "product"

    id: Mapped[intpk]
    # wb_id: Mapped[int]
    name: Mapped[str]
    price: Mapped[int] = mapped_column(default=None)
    quantity: Mapped[int] = mapped_column(default=0)
    brand: Mapped[int | None] = mapped_column(
        ForeignKey("brand.id", onupdate="SET NULL")
    )
    category: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )
    root: Mapped[int | None]
    subjectId: Mapped[int | None]
    rating: Mapped[int | None]
    pics: Mapped[dict[Any, Any]]
    # price_history: Mapped[list[dict[Any, Any]]] = mapped_column(type_=JSONB)
    price_history: Mapped[dict[Any, Any]]
    discount: Mapped[int] = mapped_column(default=0)
    # price_history_check: Mapped[bool] = mapped_column(default=False)

    repr_cols_num = 3
    repr_cols = ("category", "subjectID", "updated")

    category_relationship: Mapped["Category"] = relationship(back_populates="product")
