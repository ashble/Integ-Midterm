from models.expense import Expense
from validators.category_validator import validate_category_name


def filter_expenses_query(category_name=None):
    query = Expense.query
    if category_name:
        category = validate_category_name(category_name)  # may raise
        query = query.filter_by(category_id=category.id)
    return query
