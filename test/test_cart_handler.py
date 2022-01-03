import pytest
from src.db_build import connect_db
from src.cart_handler import base_calculation, calculate_total, create_cart, clear_carts
from test.test_product_handler import TEST_PRODUCT, TEST_PRODUCT2


def test_can_create_a_cart():
    conn = connect_db(test=True)
    with conn:
        clear_carts(conn)
        cart_id = create_cart(conn)
        c = conn.cursor()
        c.execute("SELECT cart_id FROM carts")
        actual_id = c.fetchone()[0]
        assert actual_id == cart_id


def test_can_create_two_carts():
    conn = connect_db(test=True)
    with conn:
        clear_carts(conn)
        id1 = create_cart(conn)
        id2 = create_cart(conn)
        assert id1 == 1
        assert id2 == 2


@pytest.mark.skip()
def test_can_add_product_to_cart():
    pass


def test_can_calculate_total_of_products_without_rules():
    orders = {
        "1": {
            "price": 20,
            "amount": 2
        },
        "2": {
            "price": 22,
            "amount": 1
        }
    }
    expected_total = 62
    actual_total = base_calculation(orders)
    assert actual_total == expected_total
