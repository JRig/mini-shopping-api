from test.test_products import TEST_PRODUCT
from src.database_handler import clear_products, create_db, create_product, read_product


def test_can_write_a_product_to_db():
    conn = create_db()
    with conn:
        actual_id = create_product(conn, TEST_PRODUCT)
        c = conn.cursor()
        c.execute("SELECT * FROM products;")
        assert c.fetchall() == [(
            actual_id,
            TEST_PRODUCT["title"],
            TEST_PRODUCT["description"],
            TEST_PRODUCT["price"],
            TEST_PRODUCT["currency"]
            )]


def test_can_read_a_product_from_db():
    conn = create_db()
    expected_id = 1
    expected_product = TEST_PRODUCT
    expected_product["id"] = expected_id
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
