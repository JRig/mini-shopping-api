from sqlite3 import Connection
from sqlite3.dbapi2 import DatabaseError
from src.db_build import connect_db


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
    print(f"Inserted {product}")
    c.execute(
        "SELECT product_id FROM products WHERE title = ?",
        [product["title"]])
    conn.commit()
    return c.fetchone()[0]


def read_product(conn: Connection, product_id: int):
    c = conn.cursor()
    c.execute("""
    SELECT * FROM products
    WHERE product_id = ?
    """, [product_id])
    product_raw = c.fetchall()
    if len(product_raw) == 0:
        return None
    p_id, p_title, p_descr, p_price, p_currency = product_raw[0]
    return {
        "product_id": p_id,
        "title": p_title,
        "description": p_descr,
        "price": p_price,
        "currency": p_currency
    }


def read_all_products(conn: Connection):
    c = conn.cursor()
    c.execute("""
    SELECT * FROM products
    """)
    products_raw = c.fetchall()
    products = [dict(
        product_id=p[0],
        title=p[1],
        description=p[2],
        price=p[3],
        currency=p[4]
    ) for p in products_raw]
    return products


def clear_products(conn: Connection):
    c = conn.cursor()
    c.execute("DELETE FROM products;")


def delete_product(conn: Connection, product_id: int) -> bool:
    c = conn.cursor()
    try:
        c.execute("""
        DELETE FROM products
        WHERE product_id = ?
        """, [product_id])
        conn.commit()
    except DatabaseError:
        return False
    return True


if __name__ == "__main__":
    conn = connect_db(test=True)
    with conn:
        clear_products(conn)
        c = conn.cursor()
        c.execute("""
        INSERT INTO products (title, description, price, currency)
        VALUES (
            "Manual1", "", 20, "USD"
        );
        """)
        c.execute("""
        SELECT * FROM products;
        """)
        print(c.fetchall())
        clear_products(conn)
