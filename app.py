from flask import Flask, request, jsonify, render_template

from utils.user_manager import add_user, search_user_by_phone
from utils.wallet_manager import topup_wallet
from utils.transaction_processor import process_transaction
from utils.customer_of_month import get_customer_of_month
from utils.json_storage_manager import read_data

from schemas.schemas import UserSchema, WalletTopupSchema, TransactionSchema
from marshmallow import ValidationError


app = Flask(__name__)


def get_json_data():
    data = request.get_json()
    if not data:
        raise ValidationError({"error": ["Invalid JSON body"]})
    return data


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/add_user_page")
def add_user_page():
    return render_template("add_user.html")


@app.route("/add_user", methods=["POST"])
def add_user_api():
    try:
        data = get_json_data()
        validated = UserSchema().load(data)

        result = add_user(validated["name"], validated["phone"])

        if not result["success"]:
            return jsonify({"error": result["error"]}), 400

        return jsonify({
            "message": result["data"]
        }), 201

    except ValidationError as err:
        return jsonify(err.messages), 400


@app.route("/search_user_page")
def search_user_page():
    return render_template("search_user.html")


@app.route("/user/<phone>", methods=["GET"])
def get_user_api(phone):

    result = search_user_by_phone(phone)

    if not result["success"]:
        return jsonify({"error": result["error"]}), 404

    return jsonify(result["data"]), 200


@app.route("/wallet_page")
def wallet_page():
    return render_template("wallet.html")


@app.route("/wallet/topup", methods=["POST"])
def wallet_topup_api():
    try:
        data = get_json_data()
        validated = WalletTopupSchema().load(data)

        result = topup_wallet(
            validated["phone"],
            validated["amount"]
        )

        if not result["success"]:
            return jsonify({"error": result["error"]}), 400

        return jsonify({
            "message": "Wallet updated",
            "balance": result["data"]
        }), 200

    except ValidationError as err:
        return jsonify(err.messages), 400


@app.route("/transaction_page")
def transaction_page():
    return render_template("transaction.html")


@app.route("/transaction", methods=["POST"])
def transaction_api():
    try:
        data = get_json_data()

        validated = TransactionSchema().load(data)

        result = process_transaction(
            validated["phone"],
            validated["bill_amount"],
            validated.get("promo_code")
        )

        if not result["success"]:
            return jsonify({"error": result["error"]}), 400

        return jsonify({
            "message": "Transaction successful",
            "transaction": result["data"]
        }), 201

    except ValidationError as err:
        return jsonify(err.messages), 400


@app.route("/transactions_page")
def transactions_page():
    return render_template("transactions_history.html")


@app.route("/customer_of_month", methods=["GET"])
def customer_of_month():
    customer = get_customer_of_month()

    if not customer:
        return jsonify({"error": "No customer found"}), 404

    return jsonify(customer), 200


@app.route("/transactions", methods=["GET"])
def list_transactions():

    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))
    except ValueError:
        return jsonify({"error": "Pagination parameters must be integers"}), 400

    if page <= 0 or per_page <= 0:
        return jsonify({"error": "Page and per_page must be positive numbers"}), 400

    data = read_data()

    transactions = []
    for user in data["users"]:
        transactions.extend(user.get("transactions", []))

    start = (page - 1) * per_page
    end = start + per_page

    paginated = transactions[start:end]

    total = len(transactions)
    total_pages = (total + per_page - 1) // per_page

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "data": paginated
    }), 200


if __name__ == "__main__":
    app.run(debug=True)