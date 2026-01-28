import pytest 
from decimal import Decimal
from unittest.mock import patch 
from io import StringIO

from src.main import is_field_valid, is_quit, main, create_expense, calculate_payment_split, calculate_payment_plan, print_payment_plan

def test_create_expense_returns_expense():
    """Test create_expense() with a valid expense name."""
    inputs = ['Groceries', '50.00', '15', 'yes', 'no', 'yes']
    expected_exp = {
        "name": "Groceries",
        "amount": Decimal("50.00"),
        "due_date": "15",
        "fixed_due_date": "yes",
        "is_split": "no",
        "is_active": "yes"
    }
    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            test_expense = create_expense()
            output = fake_out.getvalue()
            assert "Expense value entered: Groceries" in output

            assert test_expense == expected_exp

def test_create_expense_quits_returns_none():
    """Test create_expense() with quit command."""
    with patch('builtins.input', return_value='quit'):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            test_expense = create_expense()
            output = fake_out.getvalue()
            assert "Exiting input." in output
            assert "Expense name entered: quit" not in output 
            assert test_expense == None

def test_calculate_payment_split():
    """ Test calculate_payment_split() """
    test_expenses = [
        {"name": "expense_name_1", "amount": Decimal("407"), "due_date": "1", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_2", "amount": Decimal("165"), "due_date": "7", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_3", "amount": Decimal("270"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_4", "amount": Decimal("160"), "due_date": "", "is_split": "no", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_name_5", "amount": Decimal("330.55"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_6", "amount": Decimal("360"), "due_date": "", "is_split": "no", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_name_7", "amount": Decimal("382.02"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_8", "amount": Decimal("80"), "due_date": "5", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_9", "amount": Decimal("80"), "due_date": "28", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
    ]

    expected_exp_1 = [
        {"name": "expense_name_1", "amount": Decimal("407"), "due_date": "1", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_3", "amount": Decimal("270"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_6", "amount": Decimal("360"), "due_date": "", "is_split": "no", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_name_8", "amount": Decimal("80"), "due_date": "5", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
    ]

    expected_exp_2 = [
        {"name": "expense_name_2", "amount": Decimal("165"), "due_date": "7", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_4", "amount": Decimal("160"), "due_date": "", "is_split": "no", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_name_5", "amount": Decimal("330.55"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_7", "amount": Decimal("382.02"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_9", "amount": Decimal("80"), "due_date": "28", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
    ]

    test_exp_1, test_exp_2 = calculate_payment_split(test_expenses)

    assert test_exp_1 == expected_exp_1
    assert test_exp_2 == expected_exp_2

def test_calculate_payment_plan_with_split_expenses():
    """ Test calculate_paymennt_plan() with split expenses included """
    test_expenses = [
        {"name": "expense_split_1", "amount": Decimal("1498.59"), "due_date": "", "is_split": "yes", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_split_2", "amount": Decimal("150"), "due_date": "", "is_split": "yes", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_name_1", "amount": Decimal("407"), "due_date": "1", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_2", "amount": Decimal("165"), "due_date": "7", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_3", "amount": Decimal("270"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_4", "amount": Decimal("160"), "due_date": "", "is_split": "no", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_name_5", "amount": Decimal("330.55"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_6", "amount": Decimal("360"), "due_date": "", "is_split": "no", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_name_7", "amount": Decimal("382.02"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_8", "amount": Decimal("80"), "due_date": "5", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_9", "amount": Decimal("80"), "due_date": "28", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
    ]

    expected_exp_1 = [
        {"name": "expense_name_1", "amount": Decimal("407"), "due_date": "1", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_3", "amount": Decimal("270"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_6", "amount": Decimal("360"), "due_date": "", "is_split": "no", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_name_8", "amount": Decimal("80"), "due_date": "5", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_split_1", "amount": Decimal("1498.59"), "due_date": "", "is_split": "yes", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_split_2", "amount": Decimal("150"), "due_date": "", "is_split": "yes", "is_active": "yes", "fixed_due_date": "no"},
    ]

    expected_exp_2 = [
        {"name": "expense_name_2", "amount": Decimal("165"), "due_date": "7", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_4", "amount": Decimal("160"), "due_date": "", "is_split": "no", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_name_5", "amount": Decimal("330.55"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_7", "amount": Decimal("382.02"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_9", "amount": Decimal("80"), "due_date": "28", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_split_1", "amount": Decimal("1498.59"), "due_date": "", "is_split": "yes", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_split_2", "amount": Decimal("150"), "due_date": "", "is_split": "yes", "is_active": "yes", "fixed_due_date": "no"},
    ]

    test_exp_1, test_exp_2 = calculate_payment_plan(test_expenses)

    print(f"test_exp_1: {test_exp_1}")
    print(f"test_exp_2: {test_exp_2}")

    assert test_exp_1 == expected_exp_1
    assert test_exp_2 == expected_exp_2

def test_print_payment_plan():
    """ Test print_payment_plan() output """
    test_exp_1 = [
        {"name": "expense_name_1", "amount": Decimal("407"), "due_date": "1", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_3", "amount": Decimal("270"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_6", "amount": Decimal("360"), "due_date": "", "is_split": "no", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_name_8", "amount": Decimal("80"), "due_date": "5", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_split_1", "amount": Decimal("1498.59"), "due_date": "", "is_split": "yes", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_split_2", "amount": Decimal("150"), "due_date": "", "is_split": "yes", "is_active": "yes", "fixed_due_date": "no"},
    ]

    test_exp_2 = [
        {"name": "expense_name_2", "amount": Decimal("165"), "due_date": "7", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_4", "amount": Decimal("160"), "due_date": "", "is_split": "no", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_name_5", "amount": Decimal("330.55"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_7", "amount": Decimal("382.02"), "due_date": "10", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_name_9", "amount": Decimal("80"), "due_date": "28", "is_split": "no", "is_active": "yes", "fixed_due_date": "yes"},
        {"name": "expense_split_1", "amount": Decimal("1498.59"), "due_date": "", "is_split": "yes", "is_active": "yes", "fixed_due_date": "no"},
        {"name": "expense_split_2", "amount": Decimal("150"), "due_date": "", "is_split": "yes", "is_active": "yes", "fixed_due_date": "no"},
    ]

    with patch('sys.stdout', new=StringIO()) as fake_out:
        print_payment_plan(test_exp_1, test_exp_2)
        output = fake_out.getvalue()
        assert "-> Split Amount for expense_split_1: 749.30" in output
        assert "-> Split Amount for expense_split_2: 75.00" in output 
        assert "Difference between schedules: $0.57" in output