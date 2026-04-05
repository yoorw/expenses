from datetime import date
from decimal import Decimal, InvalidOperation
import pytest 

from src.models.expense import Expense

def test_basic_contruction():
    expense = Expense(
        name="Lunch",
        amount="12.50",
        due_date="15",
        fixed_due_date="yes",
        is_split="yes",
        is_active="yes"
    )

    assert expense.name == "Lunch"
    assert expense.amount == Decimal("12.50")
    assert expense.due_date == 15
    assert expense.fixed_due_date is True
    assert expense.is_split is True
    assert expense.is_active is True

def test_amount_validation():
    with pytest.raises(InvalidOperation):
        Expense(
            name="BadAmount",
            amount="not-a-number",
            due_date="15",
            fixed_due_date="yes",
            is_split="yes",
            is_active="yes"
        )
    
def test_to_dict():
    expense = Expense(
        name="Office Supplies",
        amount=45.00,
        due_date="15",
        fixed_due_date="yes",
        is_split="yes",
        is_active="yes"
    )
    expense_dict = expense.to_dict()

    assert expense_dict["name"] == "Office Supplies"
    assert expense_dict["amount"] == str(Decimal("45.00"))
    assert expense_dict["due_date"] == 15
    assert expense_dict["fixed_due_date"] is True
    assert expense_dict["is_split"] is True
    assert expense_dict["is_active"] is True
    

def test_expense_fields_not_all_string():
    pass

def test_due_date_outside_range():
    pass

def test_amount_negative():
    pass