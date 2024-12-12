from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, intpk


class Options(Base):
    __tablename__ = "options"

    id: Mapped[intpk]
    nm_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    card: Mapped[dict[Any, Any]]
