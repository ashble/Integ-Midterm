from flask import Blueprint, request, jsonify
from database import get_db_connection

expense_routes = Blueprint("expense_routes", __name__)


# CREATE EXPENSE

@expense_routes.route("/api/expenses", methods=["POST"])
def create_expense():

    data = request.get_json()

    description = data.get("description")
    amount = data.get("amount")
    category = data.get("category")

    if not description or amount is None or not category:
        return jsonify({
            "error": "Description, amount, and category are required."
        }), 400

    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO expenses (description, amount, category)
        VALUES (?, ?, ?)
    """, (description, amount, category))

    connection.commit()

    expense_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "message": "Expense created successfully.",
        "expense": {
            "id": expense_id,
            "description": description,
            "amount": amount,
            "category": category
        }
    }), 201
