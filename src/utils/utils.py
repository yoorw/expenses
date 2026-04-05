from decimal import Decimal, ROUND_HALF_UP

def decimal_to_currency(value: Decimal) -> Decimal:
    """Convert a Decimal value to a currency format with two decimal places."""
    return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def string_to_boolean(value: str) -> bool:
    """Convert a string to a boolean value."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value_lower = value.strip().lower()
        if value_lower in ['yes', 'y', 'true', 't', '1']:
            return True
        elif value_lower in ['no', 'n', 'false', 'f', '0']:
            return False
    raise ValueError(f"Cannot convert '{value}' to boolean.")

