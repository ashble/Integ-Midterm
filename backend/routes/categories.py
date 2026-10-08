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
