import pytest
from src.db_build import connect_db
from src.cart_handler import base_calculation, calculate_total, create_cart, clear_carts, add_order_to_cart, get_existing_orders, clear_orders
from test.test_product_handler import TEST_PRODUCT, TEST_PRODUCT2
from src.product_handler import clear_products, create_product


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


def test_can_add_product_to_cart():
    conn = connect_db(test=True)
    amount = 1
    with conn:
        clear_carts(conn)
        clear_products(conn)
        clear_orders(conn)
        product_id = create_product(conn, TEST_PRODUCT)
        cart_id = create_cart(conn)
        add_order_to_cart(conn, amount, product_id, cart_id)

        expected_orders = {
            "1": {
                "price": TEST_PRODUCT["price"],
                "amount": 1
            }
        }

        assert get_existing_orders(conn, cart_id) == expected_orders

        expected_orders2 = {
            "1": {
                "price": TEST_PRODUCT["price"],
                "amount": 2
            }
        }
        add_order_to_cart(conn, amount, product_id, cart_id)
        assert get_existing_orders(conn, cart_id) == expected_orders2


def test_can_get_existing_orders_from_cart():
    conn = connect_db(test=True)
    with conn:
        clear_carts(conn)
        clear_products(conn)
        clear_orders(conn)
        product_id = create_product(conn, TEST_PRODUCT)
        cart_id = create_cart(conn)
        existing_orders = get_existing_orders(conn, cart_id)
        assert existing_orders == {}
        c = conn.cursor()
        c.execute("""
        INSERT INTO orders (cart_id, product_id) VALUES (?, ?)
        """, [cart_id, product_id])

        expected_orders = {
            "1": {
                "price": TEST_PRODUCT["price"],
                "amount": 1
            }
        }
        actual_orders = get_existing_orders(conn, cart_id)

        assert actual_orders == expected_orders


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
