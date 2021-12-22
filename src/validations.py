from pydantic import BaseModel
from typing import Optional, List

from pydantic.error_wrappers import ValidationError


class Product(BaseModel):
    title: str
    description: Optional[str] = ""
    price: int
    currency: Optional[str] = "USD"


class Cart(BaseModel):
    products: List[Product]
    total: float


def validate_product(candidate: dict):
    try:
        Product(**candidate)
    except ValidationError as e:
        return False, e
    return True, None
