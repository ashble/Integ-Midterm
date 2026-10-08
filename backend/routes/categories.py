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

from sqlalchemy import func
from extensions import db


@categories_bp.route("/totals", methods=["GET"])
def category_totals():
    rows = (
        db.session.query(
            Category.id,
            Category.name,
            func.coalesce(func.sum(Expense.amount), 0).label("total"),
        )
        .outerjoin(Expense, Expense.category_id == Category.id)
        .group_by(Category.id, Category.name)
        .order_by(Category.name)
        .all()
    )

    data = [{"category_id": r.id, "category": r.name, "total": round(r.total, 2)}
            for r in rows]
    grand_total = round(sum(d["total"] for d in data), 2)

    return jsonify({
        "success": True,
        "data": data,
        "grand_total": grand_total,
    }), 200
