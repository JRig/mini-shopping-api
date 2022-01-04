from sqlite3.dbapi2 import Connection, DatabaseError
import sqlite3 as db


CREATE_PRODUCTS = """
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    title VARCHAR(20) UNIQUE,
    description TEXT NOT NULL,
    price INTEGER NOT NULL,
    currency VARCHAR(3) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 1
);
"""
CREATE_CARTS = """
CREATE TABLE IF NOT EXISTS carts (
    cart_id INTEGER PRIMARY KEY,
    total FLOAT
);
"""
CREATE_ORDERS = """
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    cart_id INTEGER,
    product_id INTEGER,
    amount INTEGER DEFAULT 1,
    FOREIGN KEY (cart_id)
        REFERENCES carts (cart_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
)
"""
DELETE_PRODUCTS = "DELETE FROM products;"


def create_db(conn: Connection):
    c = conn.cursor()
    c.execute(CREATE_PRODUCTS)
    c.execute(CREATE_CARTS)
    c.execute(CREATE_ORDERS)
    conn.commit()


def build_if_needed(conn: Connection):
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM products;")
        c.execute("SELECT * FROM carts;")
        c.execute("SELECT * FROM orders;")
    except DatabaseError:
        create_db(conn)


def connect_db(test=False):
    if test:
        conn: Connection = db.connect("test_minishop.db")
    else:
        conn: Connection = db.connect("minishop.db")
    build_if_needed(conn)
    return conn


if __name__ == "__main__":
    for source in ["test_minishop.db", "minishop.db"]:
        conn = db.connect(source)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS orders;")
        c.execute("DROP TABLE IF EXISTS carts;")
        c.execute("DROP TABLE IF EXISTS products;")
        conn.commit()
        conn.close()
