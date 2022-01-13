from sqlite3.dbapi2 import Connection
from src.product_handler import read_product
from src.rules import \
    maximum_100_usd_total,\
    discount_of_1_usd_above_20,\
    every_fifth_free


def create_cart(conn: Connection) -> int:
    c = conn.cursor()
    c.execute("""
        SELECT MAX(cart_id) FROM carts
    """)
    temp_id = c.fetchone()[0]
    if temp_id is None:
        new_id = 1
    else:
        new_id = temp_id + 1
    c.execute("""
        INSERT INTO carts (cart_id, total)
        VALUES (?, 0.0);
    """, [new_id])
    conn.commit()
    return new_id


def read_cart(conn: Connection, cart_id: int) -> dict:
    c = conn.cursor()
    c.execute(
        "SELECT * FROM carts WHERE cart_id = ?",
        [cart_id])
    cart_raw = c.fetchall()
    cart = dict(cart_id=cart_raw[0][0], total=cart_raw[0][1])
    return cart


def clear_carts(conn: Connection):
    c = conn.cursor()
    c.execute("DELETE FROM carts;")


def clear_orders(conn: Connection):
    c = conn.cursor()
    c.execute("DELETE FROM orders;")


def add_order_to_cart(conn: Connection, amount: int, product_id: str, cart_id: str):
    orders = get_existing_orders(conn, cart_id)
    if product_id not in orders.keys():
        product = read_product(conn, product_id)
        if not product:
            raise Exception("Product not found")
        price = product["price"]
        orders[product_id] = dict(price=price, amount=0)
    orders[product_id]["amount"] += amount
    total = calculate_total(orders)
    c = conn.cursor()
    c.execute("""
        INSERT INTO orders (cart_id, product_id, amount) VALUES (
            ?, ?, ?
        )
    """, [cart_id, product_id, amount])
    c.execute("""
        UPDATE carts
        SET total = ?
        WHERE cart_id = ?
    """, [total, cart_id])
    conn.commit()


def get_existing_orders(conn: Connection, cart_id: int) -> dict:
    c = conn.cursor()
    c.execute("""
        SELECT o.product_id, p.price, o.amount, o.cart_id, o.order_id
        FROM orders as o
        INNER JOIN products AS p ON p.product_id = o.product_id
        WHERE o.cart_id = ?
    """, [cart_id])
    orders_raw = c.fetchall()
    orders = {}
    if len(orders_raw) == 0:
        return {}
    for order in orders_raw:
        product_id = str(order[0])
        price = order[1]
        amount = order[2]
        if product_id not in orders:
            orders[product_id] = dict(price=price, amount=0)
        orders[product_id]["amount"] += amount
    return orders


def has_cart(conn: Connection, cart_id: int) -> bool:
    c = conn.cursor()
    c.execute("""
        SELECT * FROM carts
        WHERE cart_id = ?
    """, [cart_id])
    result = (len(c.fetchall()) > 0)
    return result


def get_orders_from_db(conn: Connection, cart_id: int) -> list:
    c = conn.cursor()
    c.execute("""
        SELECT * FROM orders
        WHERE cart_id = ?;
    """, [cart_id])
    orders_raw = c.fetchall()
    if not orders_raw:
        return []
    orders = [dict(
        order_id=order[0],
        product_id=order[2],
        amount=order[3]) for order in orders_raw]
    return orders


@every_fifth_free
@maximum_100_usd_total
@discount_of_1_usd_above_20
def calculate_total(orders: dict) -> float:
    return base_calculation(orders)


def base_calculation(orders: dict) -> float:
    # total = sum([order["price"] for order in orders])/1.0
    total = 0
    for _, order in orders.items():
        total += order["price"] * order["amount"]
    return total
