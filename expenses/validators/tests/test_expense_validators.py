import pytest
from decimal import Decimal

from expenses.validators.expense_validator import (
    AbstractExpenseValidator,
    NameValidator,
    AmountValidator,
    DueDayValidator,
    IsFixedValidator,
)


class TestAbstractExpenseValidator:
    """Test that AbstractExpenseValidator is abstract and cannot be instantiated."""

    def test_cannot_instantiate_abstract_class(self):
        """AbstractExpenseValidator should not be instantiable."""
        with pytest.raises(TypeError):
            AbstractExpenseValidator()

    def test_subclass_must_implement_validate(self):
        """Subclass without validate() method should raise TypeError."""
        
        class IncompleteValidator(AbstractExpenseValidator):
            pass
        
        with pytest.raises(TypeError):
            IncompleteValidator()


class TestNameValidator:
    """Test NameValidator with valid and invalid inputs."""

    def setup_method(self):
        self.validator = NameValidator()

    def test_validate_non_empty_string(self):
        """Non-empty string should be valid."""
        assert self.validator.validate("Rent") is True
        assert self.validator.validate("Internet Bill") is True
        assert self.validator.validate("a") is True

    def test_validate_strips_whitespace(self):
        """String with leading/trailing whitespace should be valid."""
        assert self.validator.validate("  Rent  ") is True
        assert self.validator.validate("\tElectricity\n") is True

    def test_reject_empty_string(self):
        """Empty string should raise ValueError."""
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            self.validator.validate("")

    def test_reject_whitespace_only_string(self):
        """Whitespace-only string should raise ValueError."""
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            self.validator.validate("   ")
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            self.validator.validate("\t\n")

    def test_reject_non_string(self):
        """Non-string types should raise ValueError."""
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            self.validator.validate(123)
        
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            self.validator.validate(None)
        
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            self.validator.validate([])


class TestAmountValidator:
    """Test AmountValidator with various numeric inputs and precision."""

    def setup_method(self):
        self.validator = AmountValidator()

    # Valid amounts
    def test_validate_positive_float(self):
        """Positive floats with up to 2 decimals should be valid."""
        assert self.validator.validate(50.00) is True
        assert self.validator.validate(13.51) is True
        assert self.validator.validate(0.01) is True
        assert self.validator.validate(99.9) is True

    def test_validate_positive_int(self):
        """Positive integers should be valid."""
        assert self.validator.validate(100) is True
        assert self.validator.validate(1) is True
        assert self.validator.validate(0) is True

    def test_validate_positive_string(self):
        """String representations of valid amounts should be valid."""
        assert self.validator.validate("50.00") is True
        assert self.validator.validate("13.51") is True
        assert self.validator.validate("100") is True

    def test_validate_decimal(self):
        """Decimal instances should be valid."""
        assert self.validator.validate(Decimal("50.00")) is True
        assert self.validator.validate(Decimal("13.51")) is True

    def test_validate_no_decimal_places(self):
        """Amounts with no decimal places should be valid."""
        assert self.validator.validate(100) is True
        assert self.validator.validate("50") is True

    # Invalid amounts - precision
    def test_reject_incorrect_decimal_places(self):
        """Amounts with more than 2 decimal places should raise ValueError."""
        with pytest.raises(ValueError, match="Amount must have at least 2 decimal places"):
            self.validator.validate(13.511)
        
        with pytest.raises(ValueError, match="Amount must have at least 2 decimal places"):
            self.validator.validate("13.5111")
        
        with pytest.raises(ValueError, match="Amount must have at least 2 decimal places"):
            self.validator.validate(Decimal("0.001"))
        
        with pytest.raises(ValueError, match="Amount must have at least 2 decimal places"):
            self.validator.validate(Decimal(13.51))


    # Invalid amounts - negative
    def test_reject_negative_amount(self):
        """Negative amounts should raise ValueError."""
        with pytest.raises(ValueError, match="Amount must be non-negative"):
            self.validator.validate(-5)
        
        with pytest.raises(ValueError, match="Amount must be non-negative"):
            self.validator.validate("-13.50")
        
        with pytest.raises(ValueError, match="Amount must be non-negative"):
            self.validator.validate(Decimal("-0.01"))

    # Invalid amounts - non-numeric
    def test_reject_non_numeric_string(self):
        """Non-numeric strings should raise ValueError."""
        with pytest.raises(ValueError, match="Amount must be a number or Decimal"):
            self.validator.validate("abc")
        
        with pytest.raises(ValueError, match="Amount must be a number or Decimal"):
            self.validator.validate("12.34.56")

    def test_reject_non_numeric_types(self):
        """Non-numeric types should raise ValueError."""
        with pytest.raises(ValueError, match="Amount must be a number or Decimal"):
            self.validator.validate(None)
        
        with pytest.raises(ValueError, match="Amount must be a number or Decimal"):
            self.validator.validate([])
        
        with pytest.raises(ValueError, match="Amount must be a number or Decimal"):
            self.validator.validate({})


class TestDueDayValidator:
    """Test DueDayValidator with valid and invalid day ranges."""

    def setup_method(self):
        self.validator = DueDayValidator()

    def test_validate_valid_days(self):
        """Days 1-31 should be valid."""
        assert self.validator.validate(1) is True
        assert self.validator.validate(15) is True
        assert self.validator.validate(31) is True

    def test_validate_boundary_days(self):
        """First and last days should be valid."""
        assert self.validator.validate(1) is True
        assert self.validator.validate(31) is True

    def test_reject_day_zero(self):
        """Day 0 should raise ValueError."""
        with pytest.raises(ValueError, match="Due day must be between 1 and 31"):
            self.validator.validate(0)

    def test_reject_day_negative(self):
        """Negative days should raise ValueError."""
        with pytest.raises(ValueError, match="Due day must be between 1 and 31"):
            self.validator.validate(-1)
        
        with pytest.raises(ValueError, match="Due day must be between 1 and 31"):
            self.validator.validate(-15)

    def test_reject_day_over_31(self):
        """Days above 31 should raise ValueError."""
        with pytest.raises(ValueError, match="Due day must be between 1 and 31"):
            self.validator.validate(32)
        
        with pytest.raises(ValueError, match="Due day must be between 1 and 31"):
            self.validator.validate(100)

    def test_reject_non_integer(self):
        """Non-integer types should raise ValueError."""
        with pytest.raises(ValueError, match="Due day must be an integer"):
            self.validator.validate(15.5)
        
        with pytest.raises(ValueError, match="Due day must be an integer"):
            self.validator.validate("15")
        
        with pytest.raises(ValueError, match="Due day must be an integer"):
            self.validator.validate(None)


class TestIsFixedValidator:
    """Test IsFixedValidator with boolean inputs."""

    def setup_method(self):
        self.validator = IsFixedValidator()

    def test_validate_true(self):
        """Boolean True should be valid."""
        assert self.validator.validate(True) is True

    def test_validate_false(self):
        """Boolean False should be valid."""
        assert self.validator.validate(False) is True

    def test_reject_non_boolean_int(self):
        """Integer 0 or 1 should raise ValueError (even though they're truthy/falsy)."""
        with pytest.raises(ValueError, match="is_fixed must be a boolean value"):
            self.validator.validate(0)
        
        with pytest.raises(ValueError, match="is_fixed must be a boolean value"):
            self.validator.validate(1)

    def test_reject_non_boolean_string(self):
        """String "true" or "false" should raise ValueError."""
        with pytest.raises(ValueError, match="is_fixed must be a boolean value"):
            self.validator.validate("true")
        
        with pytest.raises(ValueError, match="is_fixed must be a boolean value"):
            self.validator.validate("false")

    def test_reject_non_boolean_none(self):
        """None should raise ValueError."""
        with pytest.raises(ValueError, match="is_fixed must be a boolean value"):
            self.validator.validate(None)

    def test_reject_non_boolean_list(self):
        """Non-boolean types should raise ValueError."""
        with pytest.raises(ValueError, match="is_fixed must be a boolean value"):
            self.validator.validate([])
        
        with pytest.raises(ValueError, match="is_fixed must be a boolean value"):
            self.validator.validate({})


class TestValidatorsIntegration:
    """Integration tests for all validators working together."""

    def test_all_validators_valid_data(self):
        """All validators should accept valid data."""
        name_validator = NameValidator()
        amount_validator = AmountValidator()
        due_day_validator = DueDayValidator()
        is_fixed_validator = IsFixedValidator()
        
        assert name_validator.validate("Rent") is True
        assert amount_validator.validate(1500.00) is True
        assert due_day_validator.validate(1) is True
        assert is_fixed_validator.validate(True) is True

    def test_all_validators_reject_invalid_data(self):
        """All validators should reject invalid data."""
        name_validator = NameValidator()
        amount_validator = AmountValidator()
        due_day_validator = DueDayValidator()
        is_fixed_validator = IsFixedValidator()
        
        with pytest.raises(ValueError):
            name_validator.validate("")
        
        with pytest.raises(ValueError):
            amount_validator.validate(-100)
        
        with pytest.raises(ValueError):
            due_day_validator.validate(32)
        
        with pytest.raises(ValueError):
            is_fixed_validator.validate("yes")
