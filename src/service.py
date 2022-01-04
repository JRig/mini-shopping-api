import json
from sqlite3.dbapi2 import Connection
from flask import Flask, request, g, make_response, current_app
from flask.wrappers import Response
from src.cart_handler import add_order_to_cart, create_cart, get_orders_from_db, read_cart
from src.validations import validate_product, validate_order, Order
from src.product_handler import delete_product, read_product, create_product, read_all_products
from src.db_build import connect_db


def app():
    flask_app = Flask(__name__)

    def get_db() -> Connection:
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = connect_db()
        return db

    @flask_app.route("/product/<id>", methods=["GET"])
    def get_product(id):
        product = read_product(get_db(), id)
        if not product:
            return {"Error": "Product not found."}, 404
        return product, 200

    @flask_app.route("/product", methods=["GET"])
    def get_all_product():
        products = read_all_products(get_db())
        return {"products": products}, 200

    @flask_app.route("/product/<id>", methods=["DELETE"])
    def remove_product(id):
        deleted = delete_product(get_db(), id)
        if not deleted:
            return {"Error": "Could not delete ressource."}, 500
        response = make_response('', 204)
        response.mimetype = current_app.config['JSONIFY_MIMETYPE']
        return response

    @flask_app.route("/product", methods=["POST"])
    def new_product():
        content = request.json
        if not content:
            return dict(error="Content not JSON"), 400
        validated, err_msg = validate_product(content)
        if not validated:
            return dict(error=err_msg), 400
        product_id = create_product(get_db(), content)
        return dict(product_id=product_id), 200

    @flask_app.route("/cart", methods=["POST"])
    def new_cart():
        cart_id = create_cart(get_db())
        return dict(cart_id=cart_id, total=0)

    @flask_app.route("/cart/<id>", methods=["GET"])
    def get_cart(id):
        try:
            cart = read_cart(get_db(), id)
        except Exception:
            return {"Error": "Cart not found."}, 404
        return cart

    @flask_app.route("/cart/<cart_id>/add", methods=["POST"])
    def order_to_cart(cart_id):
        content = request.json
        if not content:
            return dict(error="Content not JSON"), 400
        validated, err_msg = validate_order(content)
        if not validated:
            return dict(error=err_msg), 400
        order = Order(**content)
        add_order_to_cart(get_db(), order.amount, order.product_id, cart_id)
        response = make_response('', 204)
        response.mimetype = current_app.config['JSONIFY_MIMETYPE']
        return response

    @flask_app.route("/cart/<cart_id>/orders", methods=["GET"])
    def show_orders(cart_id):
        orders = get_orders_from_db(get_db(), cart_id)
        return Response(json.dumps(orders),  mimetype='application/json')

    @flask_app.teardown_appcontext
    def close_connection(exception):
        db: Connection = getattr(g, '_database', None)
        if db is not None:
            db.close()

    return flask_app


if __name__ == "__main__":
    app().run(debug=False)
