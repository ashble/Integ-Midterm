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
