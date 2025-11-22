from decimal import Decimal

# from expenses.models.expense import Expense
from expenses.validators.expense_validator import (
    NameValidator,
    AmountValidator,
    DueDayValidator,
    IsFixedValidator
)

# def create_expense(
#     name: str,
#     amount: any,
#     due_day: int,
#     is_fixed: bool
# ) -> Expense:
#     """Create and return an Expense object after validating inputs."""
    
#     try:
#         # Validate inputs
#         NameValidator().validate(name)
#         AmountValidator().validate(amount)
#         DueDayValidator().validate(due_day)
#         IsFixedValidator().validate(is_fixed)

#     except ValueError as ve:
#         # if any Validator fails, return error response
#         return {"error": str(ve)}
    
#     # Create and return Expense object
#     return Expense(
#         name=name,
#         amount=Decimal(str(amount)),
#         due_day=due_day,
#         is_fixed=is_fixed
#     )

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

def clean_is_fixed(is_fixed: bool) -> bool:
    """Clean and return the is_fixed value as a boolean."""

    try:
        IsFixedValidator().validate(is_fixed)
    except ValueError as ve:
        raise ve

    return is_fixed
