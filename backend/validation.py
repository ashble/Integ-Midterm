# =========================================================
# VAL-BE-01: Validate expense amount
# =========================================================

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


# =========================================================
# VAL-BE-03: Prevent negative amounts
# =========================================================

def validate_non_negative_amount(amount):
    if amount is None:
        return None

    try:
        value = Decimal(str(amount))

        if value < 0:
            return "Amount cannot be negative."

        return None

    except (InvalidOperation, ValueError):
        return "Amount must be a valid number."


# =========================================================
# Combine VAL-BE-01, VAL-BE-02, and VAL-BE-03
# =========================================================

def validate_expense(data):
    errors = {}

    # VAL-BE-02
    required_errors = validate_required_fields(data)
    errors.update(required_errors)

    # Only validate amount if it was provided
    if "amount" in data and data["amount"] is not None:

        # VAL-BE-01
        amount_error = validate_amount(data["amount"])

        if amount_error:
            errors["amount"] = amount_error

        else:
            # VAL-BE-03
            negative_error = validate_non_negative_amount(data["amount"])

            if negative_error:
                errors["amount"] = negative_error

    return errors


# =========================================================
# VAL-BE-05: Standardize API success responses
# =========================================================

def success_response(message, data=None, status_code=200):

    response = {
        "success": True,
        "message": message
    }

    if data is not None:
        response["data"] = data

    return jsonify(response), status_code


# =========================================================
# VAL-BE-04 + VAL-BE-05:
# API error handling + standard error responses
# =========================================================

def error_response(message, errors=None, status_code=400):

    response = {
        "success": False,
        "message": message
    }

    if errors:
        response["errors"] = errors

    return jsonify(response), status_code
