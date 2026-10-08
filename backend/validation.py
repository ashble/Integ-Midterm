def validate_amount(amount):
    if amount is None:
        return "Amount is required."

    try:
        if isinstance(amount, bool):
            return "Amount must be a valid number."

        value = Decimal(str(amount))

        if not value.is_finite():
            return "Amount must be a valid number."

        return None

    except (InvalidOperation, ValueError):
        return "Amount must be a valid number."


# =========================================================
# VAL-BE-02: Validate required fields
# =========================================================

def validate_required_fields(data):
    errors = {}

    required_fields = ["title", "amount", "category"]

    for field in required_fields:

        if field not in data:
            errors[field] = f"{field} is required."

        elif data[field] is None:
            errors[field] = f"{field} is required."

        elif isinstance(data[field], str) and not data[field].strip():
            errors[field] = f"{field} cannot be empty."

    return errors
