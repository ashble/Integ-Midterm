from models.category import Category


class CategoryValidationError(ValueError):
    """Raised when a category value is missing or invalid."""


def validate_category_id(value):
    """Return the Category for a valid id, or raise CategoryValidationError."""
    if value is None or value == "":
        raise CategoryValidationError("category_id is required.")

    try:
        category_id = int(value)
    except (TypeError, ValueError):
        raise CategoryValidationError("category_id must be an integer.")

    category = Category.query.get(category_id)
    if category is None:
        raise CategoryValidationError(f"Category {category_id} does not exist.")
    return category


def validate_category_name(name):
    """Return the Category for a valid name (case-insensitive), or raise."""
    if not name or not str(name).strip():
        raise CategoryValidationError("category name is required.")

    category = Category.query.filter(
        Category.name.ilike(str(name).strip())
    ).first()
    if category is None:
        raise CategoryValidationError(f"Unknown category '{name}'.")
    return category

from validators.category_validator import validate_category_id, CategoryValidationError

try:
    category = validate_category_id(data.get("category_id"))
except CategoryValidationError as e:
    return jsonify({"success": False, "error": str(e)}), 400
