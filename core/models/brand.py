from sqlalchemy.orm import Mapped

from .base import Base, intpk


class Brand(Base):
    __tablename__ = "brand"

    id: Mapped[intpk]
    wb_id: Mapped[int]
    name: Mapped[str]
