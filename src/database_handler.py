import sqlite3 as db
from sqlite3 import Connection

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    title VARCHAR(20) UNIQUE,
    description TEXT NOT NULL,
    price INTEGER NOT NULL,
    currency VARCHAR(3) NOT NULL
);
"""
DELETE_TABLE = "DELETE FROM products;"


def create_db():
    conn: Connection = db.connect("minishop.db")
    c = conn.cursor()
    c.execute(CREATE_TABLES)
    c.execute(DELETE_TABLE)
    return conn


def create_product(conn: Connection, product: dict):
    c = conn.cursor()
    c.execute("""
    INSERT INTO products (title, description, price, currency)
    VALUES (
        ?, ?, ?, ?
    );
    """, [
        product["title"],
        product["description"],
        product["price"],
        product["currency"]
        ])
    c.execute(
        "SELECT product_id FROM products WHERE title = ?",
        [product["title"]])
    return c.fetchone()[0]


def read_product(conn: Connection, product_id: int):
    c = conn.cursor()
    c.execute("""
    SELECT * FROM products
    WHERE product_id = ?
    """, [product_id])
    product_raw = c.fetchall()
    p_id, p_title, p_descr, p_price, p_currency = product_raw[0]
    return {
        "id": p_id,
        "title": p_title,
        "description": p_descr,
        "price": p_price,
        "currency": p_currency
    }


def clear_products(conn: Connection):
    c = conn.cursor()
    c.execute("DELETE FROM products;")


if __name__ == "__main__":
    conn = create_db()
    with conn:
        clear_products(conn)
        c = conn.cursor()
        c.execute("""
        INSERT INTO products (title, description, price, currency)
        VALUES (
            "Product1", "", 20, "USD"
        );
        """)
        c.execute("""
        SELECT * FROM products;
        """)
        print(c.fetchall())
        clear_products(conn)
