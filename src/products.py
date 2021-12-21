from src.database_handler import read_product, create_product

products = {}


def read_product_by_id(id: int) -> dict:
    product = read_product(id)
    return product


def create_product_in_db(data: dict):
    product_id = create_product(data)
    return product_id
