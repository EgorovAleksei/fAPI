from pydantic import BaseModel


class ProductBase(BaseModel):

    name: str
    price: int
    quantity: int
    brand: int | None
    category: int
    root: int | None
    subjectId: int | None
    rating: int | None
    pics: dict | None
    price_history: list | None
    discount: int
    # price_history_check: bool


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(ProductCreate):
    name: str | None = None
    price: int | None = None
    quantity: int | None = None
    brand: int | None = None
    category: int | None = None
    root: int | None = None
    subjectId: int | None = None
    rating: int | None = None
    pics: dict | None = None
    price_history: list | None = None
    discount: int | None = None


class Product(ProductBase):
    id: int
