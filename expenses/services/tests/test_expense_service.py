import pytest
from decimal import Decimal

from services.expense_service import (
    clean_name,
    clean_amount,
    clean_due_day,
    clean_is_fixed
)

class TestCleanName:
    def test_clean_name_valid(self):
        name = "  Grocery Shopping  "
        cleaned = clean_name(name)
        assert cleaned == "Grocery Shopping"

    def test_clean_name_invalid(self):
        with pytest.raises(ValueError):
            clean_name("   ")

class TestCleanAmount:
    def test_clean_amount_valid_string(self):
        amount = "123.40"
        cleaned = clean_amount(amount)
        assert cleaned == Decimal("123.40")

    def test_clean_amount_valid_float(self):
        amount = 123.40
        cleaned = clean_amount(amount)
        assert cleaned == Decimal("123.40")

    def test_clean_amount_valid_int(self):
        amount = 123
        cleaned = clean_amount(amount)
        assert cleaned == Decimal("123.00")

    def test_error_amount_has_incorrect_decimal_places(self):
        with pytest.raises(ValueError, match={"error": "Amount must have 2 decimal places"}):
            clean_amount("123.46")

        with pytest.raises(ValueError):
            clean_amount("123.4")

    def test_error_clean_amount_alpha_chars(self):
        with pytest.raises(ValueError):
            clean_amount("not-a-number")

class TestCleanDueDay:
    def test_clean_due_day_valid(self):
        due_day = 15
        cleaned = clean_due_day(due_day)
        assert cleaned == 15

    def test_error_due_day_too_low(self):
        with pytest.raises(ValueError):
            clean_due_day(0)

    def test_error_due_day_too_high(self):
        with pytest.raises(ValueError):
            clean_due_day(32)

    def test_error_due_day_not_integer(self):
        with pytest.raises(ValueError):
            clean_due_day("fifteen")

class TestCleanIsFixed:
    def test_clean_is_fixed_valid_true(self):
        is_fixed = True
        cleaned = clean_is_fixed(is_fixed)
        assert cleaned is True

    def test_clean_is_fixed_valid_false(self):
        is_fixed = False
        cleaned = clean_is_fixed(is_fixed)
        assert cleaned is False

    def test_error_is_fixed_not_boolean(self):
        with pytest.raises(ValueError):
            clean_is_fixed("yes")