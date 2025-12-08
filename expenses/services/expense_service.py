from decimal import Decimal

from expenses.validators.expense_validator import (
    NameValidator,
    AmountValidator,
    DueDayValidator,
    IsFixedValidator
)

def clean_name(name: str) -> str:
    """Clean and return the expense name."""

    try:
        NameValidator().validate(name)
    except ValueError as ve:
        raise ve

    return name.strip()

def clean_amount(amount: any) -> Decimal:
    """Convert and return the amount as a Decimal with 2 decimal places."""

    try:
        AmountValidator().validate(amount)
    except ValueError as ve:
        raise ve

    dec = Decimal(str(amount))
    return dec.quantize(Decimal("0.01"))

def clean_due_day(due_day: int) -> int:
    """Clean and return the due day as an integer."""

    try:
        DueDayValidator().validate(due_day)
    except ValueError as ve:
        raise ve

    return due_day

def clean_enforce_due_day(enforce_due_day: bool) -> bool:
    """Clean and return the enforce_due_day value as a boolean."""

    try:
        IsFixedValidator().validate(enforce_due_day)
    except ValueError as ve:
        raise ve

    return enforce_due_day
