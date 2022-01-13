from pydantic import BaseModel
from typing import Optional, List

from pydantic.error_wrappers import ValidationError


class Product(BaseModel):
    title: str
    description: Optional[str] = ""
    price: int
    currency: Optional[str] = "USD"


class Order(BaseModel):
    amount: int = 1
    product_id: int


class Cart(BaseModel):
    orders: List[Order]
    total: float


def validate_product(candidate: dict):
    try:
        Product(**candidate)
    except ValidationError as e:
        return False, e
    return True, None


def validate_order(candidate: dict):
    try:
        Order(**candidate)
    except ValidationError as e:
        return False, e
    return True, None
