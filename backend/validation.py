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
