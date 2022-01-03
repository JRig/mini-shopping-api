from test.test_product_validation import TEST_PRODUCT, TEST_PRODUCT2
from src.product_handler import clear_products, create_product, delete_product, read_all_products, read_product
from src.db_build import connect_db


def test_can_write_a_product_to_db():
    conn = connect_db(test=True)
    with conn:
        clear_products(conn)
        actual_id = create_product(conn, TEST_PRODUCT)
        c = conn.cursor()
        c.execute("SELECT * FROM products;")
        assert c.fetchall() == [(
            actual_id,
            TEST_PRODUCT["title"],
            TEST_PRODUCT["description"],
            TEST_PRODUCT["price"],
            TEST_PRODUCT["currency"],
            TEST_PRODUCT["stock"]
            )]


def test_can_write_two_products_to_db():
    conn = connect_db(test=True)
    with conn:
        clear_products(conn)
        id1 = create_product(conn, TEST_PRODUCT)
        id2 = create_product(conn, TEST_PRODUCT2)
        assert id1 == 1
        assert id2 == 2
        c = conn.cursor()
        c.execute("SELECT * FROM products;")
        assert len(c.fetchall()) == 2


def test_can_read_a_product_from_db():
    conn = connect_db(test=True)
    clear_products(conn)
    expected_id = 1
    expected_product = TEST_PRODUCT.copy()
    expected_product["product_id"] = expected_id
    with conn:
        c = conn.cursor()
        c.execute("""
        INSERT INTO products (title, description, price, currency)
        VALUES (
            ?, ?, ?, ?
        );
        """, [
            TEST_PRODUCT["title"],
            TEST_PRODUCT["description"],
            TEST_PRODUCT["price"],
            TEST_PRODUCT["currency"]])

        actual_product = read_product(conn, expected_id)

        assert actual_product == expected_product


def test_can_read_all_products():
    conn = connect_db(test=True)
    with conn:
        clear_products(conn)
        c = conn.cursor()
        c.execute("""
        INSERT INTO products (title, description, price, currency)
        VALUES (
            ?, ?, ?, ?
        );
        """, [
            TEST_PRODUCT["title"],
            TEST_PRODUCT["description"],
            TEST_PRODUCT["price"],
            TEST_PRODUCT["currency"]])
        c.execute("""
        INSERT INTO products (title, description, price, currency)
        VALUES (
            ?, ?, ?, ?
        );
        """, [
            TEST_PRODUCT2["title"],
            TEST_PRODUCT2["description"],
            TEST_PRODUCT2["price"],
            TEST_PRODUCT2["currency"]])
        products = read_all_products(conn)
        expected_products = [TEST_PRODUCT, TEST_PRODUCT2]
        expected_products[0]["product_id"] = 1
        expected_products[1]["product_id"] = 2
        assert products == expected_products


def test_can_delete_created_product_from_db():
    conn = connect_db(test=True)
    with conn:
        clear_products(conn)
        product_id = create_product(conn, TEST_PRODUCT)
        assert product_id == 1
        c = conn.cursor()
        c.execute(
            "SELECT product_id FROM products WHERE product_id = ?",
            [product_id])
        assert len(c.fetchall()) == 1

        delete_product(conn, product_id)

        c.execute(
            "SELECT product_id FROM products WHERE product_id = ?",
            [product_id])
        assert len(c.fetchall()) == 0
