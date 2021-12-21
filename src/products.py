from sqlite3.dbapi2 import DatabaseError
from src.database_handler import delete_product, read_product, create_product

products = {}


def read_product_by_id(id: int) -> dict:
    product = read_product(id)
    return product


def create_product_in_db(data: dict) -> int:
    product_id = create_product(data)
    return product_id


def delete_product_from_db(id: int) -> bool:
    try:
        delete_product(id)
    except DatabaseError:
        return False
    return True
