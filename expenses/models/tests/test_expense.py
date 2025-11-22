from datetime import date
from decimal import Decimal
import pytest 

from expenses.models.expense import Expense

def test_basic_contruction():
    expense = Expense(
        name="Lunch",
        amount=12.5,
        due_day=15,
        is_fixed=True
    )

    assert expense.name == "Lunch"
    assert expense.amount == Decimal("12.50")
    assert expense.due_day == 15
    assert expense.is_fixed is True

def test_to_dict_decimal_amount():
    expense = Expense(
        name="Office Supplies",
        amount=Decimal(45.00),
        due_day=20,
        is_fixed=False
    )
    expense_dict = expense.to_dict()

    assert expense_dict["name"] == "Office Supplies"
    assert expense_dict["amount"] == str(Decimal("45.00"))
    assert expense_dict["due_day"] == 20
    assert expense_dict["is_fixed"] is False

def test_to_dict_string_amount():
    expense = Expense(
        name="Office Supplies",
        amount=Decimal("45.00"),
        due_day=20,
        is_fixed=False
    )
    expense_dict = expense.to_dict()

    assert expense_dict["name"] == "Office Supplies"
    assert expense_dict["amount"] == str(Decimal("45.00"))
    assert expense_dict["due_day"] == 20
    assert expense_dict["is_fixed"] is False
