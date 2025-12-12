import pytest 
from unittest.mock import patch, MagicMock
from decimal import Decimal

from main import add_expense, get_valid_input
from expenses.services.expense_service import (
    clean_name,
)


def test_add_expense_with_mocked_clean_name(monkeypatch):
  """Test add_expense() function with mocked clean_name()."""
  
  # Mock clean_name to return a test string
  mock_clean_name = MagicMock(return_value="Test Expense")
  monkeypatch.setattr("main.clean_name", mock_clean_name)
  
  # Mock clean_amount to return a Decimal
  mock_clean_amount = MagicMock(return_value=Decimal("50.00"))
  monkeypatch.setattr("main.clean_amount", mock_clean_amount)
  
  # Mock clean_due_day to return an int
  mock_clean_due_day = MagicMock(return_value=15)
  monkeypatch.setattr("main.clean_due_day", mock_clean_due_day)
  
  # Mock clean_is_fixed to return a bool
  mock_clean_is_fixed = MagicMock(return_value=True)
  monkeypatch.setattr("main.clean_is_fixed", mock_clean_is_fixed)
  
  # Mock get_valid_input to return test inputs in sequence
  inputs = ["Test Expense", "50.00", "15", "yes"]
  mock_get_valid_input = MagicMock(side_effect=inputs)
  monkeypatch.setattr("main.get_valid_input", mock_get_valid_input)
  
  # Call add_expense
  expense = add_expense()
  
  # Assertions
  assert expense is not None
  assert expense.name == "Test Expense"
  assert expense.amount == Decimal("50.00")
  assert expense.due_day == 15
  assert expense.is_fixed is True
  
  # Verify clean_name was called with the correct input
  mock_clean_name.assert_called_once_with("Test Expense")


def test_add_expense_with_mocked_clean_name_only(monkeypatch):
  """Test add_expense() with only clean_name() mocked, other cleaners return expected values."""
  
  # Mock only clean_name to return "Gym Membership"
  mock_clean_name = MagicMock(return_value="Gym Membership")
  monkeypatch.setattr("main.clean_name", mock_clean_name)
  
  # Mock other clean functions
  monkeypatch.setattr("main.clean_amount", MagicMock(return_value=Decimal("45.99")))
  monkeypatch.setattr("main.clean_due_day", MagicMock(return_value=10))
  monkeypatch.setattr("main.clean_is_fixed", MagicMock(return_value=False))
  
  # Mock get_valid_input
  monkeypatch.setattr("main.get_valid_input", MagicMock(side_effect=["Gym", "45.99", "10", "no"]))
  
  # Call add_expense
  expense = add_expense()
  
  # Verify the mocked clean_name was used and returned the expected value
  assert expense.name == "Gym Membership"
  mock_clean_name.assert_called_once()


def test_add_expense_repeat_invalid_name():
    