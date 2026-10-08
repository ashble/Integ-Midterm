from flask import Blueprint, jsonify
from models.category import Category

categories_bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@categories_bp.route("", methods=["GET"])
def list_categories():
    categories = Category.query.order_by(Category.name).all()
    return jsonify({
        "success": True,
        "data": [c.to_dict() for c in categories],
    }), 200

from flask import request
from models.expense import Expense
from validators.category_validator import (
    validate_category_id, validate_category_name, CategoryValidationError,
)


@categories_bp.route("/<int:category_id>/expenses", methods=["GET"])
def expenses_by_category(category_id):
    try:
        category = validate_category_id(category_id)
    except CategoryValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 404

    expenses = (
        Expense.query.filter_by(category_id=category.id)
        .order_by(Expense.date.desc())
        .all()
    )
    return jsonify({
        "success": True,
        "category": category.to_dict(),
        "data": [e.to_dict() for e in expenses],
    }), 200

