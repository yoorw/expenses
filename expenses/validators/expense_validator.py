from abc import ABC, abstractmethod

class AbstractExpenseValidator(ABC):
    @abstractmethod
    def validate(self, data):
        """Validate the given expense data.
        
        Args:
            data (any): data value to be validated.
        
        Returns:
            bool: True if the data is valid, False otherwise.
        """
        pass

class NameValidator(AbstractExpenseValidator):
    def validate(self, data):
        if not isinstance(data, str) or not data.strip():
            raise ValueError("Name must be a non-empty string")
        return True 
    
class AmountValidator(AbstractExpenseValidator):
    def validate(self, data):
        from decimal import Decimal, InvalidOperation

        try:
            if isinstance(data, Decimal):
                dec = data
            else:
                dec = Decimal(str(data))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError(f"Amount must be a number or Decimal: {exc}")
        
        if dec < 0:
            raise ValueError("Amount must be non-negative")
        
        # Validate decimal places: at most 2 decimal places
        # Exponent < -2 means more than 2 decimal places
        # (e.g., 13.511 has exponent -3)
        if dec.as_tuple().exponent < -2:
            raise ValueError("Amount must have at least 2 decimal places")
        
        return True
    
class DueDayValidator(AbstractExpenseValidator):
    def validate(self, data):
        if not isinstance(data, int):
            raise ValueError("Due day must be an integer")
        if not (1 <= data <= 31):
            raise ValueError("Due day must be between 1 and 31")
        return True

class IsFixedValidator(AbstractExpenseValidator):
    def validate(self, data) -> bool:
        if data.lower() not in ("yes", "y", "true", "1", "no", "n", "false", "0"):
            raise ValueError("is_fixed must be a boolean value")
        return True
