import pytest
from unittest.mock import MagicMock
import src.products as products

TEST_PRODUCT = {
        "title": "Product1",
        "description": "My description",
        "price": 20,
        "currency": "USD"
    }


def test_can_create_new_product():
    # Well, this is just a silly test now
    products.create_product = MagicMock(return_value=1)
    id = products.create_product_in_db(TEST_PRODUCT)
    assert id == 1


def test_can_read_a_product():
    products.read_product = MagicMock(return_value=TEST_PRODUCT)
    prod = products.read_product_by_id(1)
    expected_title = "Product1"
    expected_price = 20
    assert prod["title"] == expected_title
    assert prod["price"] == expected_price


@pytest.mark.skip()
def test_can_read_all_products():
    pass


@pytest.mark.skip()
def test_can_delete_a_product():
    pass
