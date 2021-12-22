from flask import Flask, request, g, make_response, current_app
import sqlite3
from src.validations import validate_product
from src.product_handler import delete_product, read_product, create_product, read_all_products
from src.db_build import connect_db

def app():
    flask_app = Flask(__name__)

    def get_db():
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
        print(f"Incoming content: {content}")
        if not content:
            return dict(error="Content not JSON"), 400
        validated, err_msg = validate_product(content)
        if not validated:
            return dict(error=err_msg), 400
        product_id = create_product(get_db(), content)
        return dict(product_id=product_id), 200

    @flask_app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    return flask_app


if __name__ == "__main__":
    app().run(debug=False)
