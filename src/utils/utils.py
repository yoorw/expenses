from decimal import Decimal, ROUND_HALF_UP

def decimal_to_currency(value: Decimal) -> Decimal:
    """Convert a Decimal value to a currency format with two decimal places."""
    return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)