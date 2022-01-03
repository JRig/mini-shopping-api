from sqlite3.dbapi2 import Connection
from typing import List
from src.rules import \
    maximum_100_usd_total,\
    discount_of_1_usd_above_20


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
    return new_id


def clear_carts(conn: Connection):
    c = conn.cursor()
    c.execute("DELETE FROM carts;")


def add_order_to_cart(conn, amount, product_id, cart_id):
    c = conn.cursor()
    existing_orders = get_existing_orders(conn, cart_id)
    # if product_id not in existing_orders:
    #     existing_orders[product_id] = dict(price=0, amount=0)
    
    
    # calculate new total (with rules)
        # get existing orders in cart
    # insert if no rules are violated


def get_existing_orders(conn: Connection, cart_id: int) -> dict:
    c = conn.cursor()
    c.execute("""
        SELECT o.product_id, p.price, o.amount, o.cart_id, o.order_id
        FROM orders as o
        INNER JOIN products AS p ON p.product_id = o.product_id
        WHERE o.cart_id = ?
    """, [cart_id])
    orders_raw = c.fetchall()
    if orders_raw[0] is None:
        return None
    orders = {}
    for order in orders_raw:
        product_id = str(order[0])
        price = order[1]
        amount = order[2]
        if product_id not in orders:
            orders[product_id] = dict(price=0, amount=0)
        orders[product_id]["price"] += price
        orders[product_id]["amount"] += amount
    return orders


@discount_of_1_usd_above_20
def calculate_total(orders: dict) -> float:
    return base_calculation(orders)


def base_calculation(orders: dict) -> float:
    # total = sum([order["price"] for order in orders])/1.0
    total = 0
    for _, order in orders.items():
        total += order["price"] * order["amount"]
    return total
