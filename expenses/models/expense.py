from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Optional, Dict, Any


class Expense:
    """Represent a single expense item.

    Attributes
    - title: short description of the expense
    - amount: Decimal monetary amount (must be >= 0)
    - currency: ISO-style currency code (default: 'USD')
    - date: date of the expense (defaults to today)
    - category: optional category string (e.g., 'travel', 'meals')
    - notes: optional longer text
    - paid: whether the expense was paid
    """

    def __init__(
        self,
        name: str,
        amount: Any,
        due_day: int,
        is_fixed: bool,
    ) -> None:
        # Basic validation and assignments
        self.name = name
        self.amount = amount
        self.due_day = due_day
        self.is_fixed = is_fixed


    # name
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()

    # amount (store as Decimal)
    @property
    def amount(self) -> Decimal:
        return self._amount

    @amount.setter
    def amount(self, value: Any) -> None:
        try:
            # Accept Decimal, int, float, or numeric string
            if isinstance(value, Decimal):
                dec = value
            else:
                dec = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError(f"amount must be a number or Decimal: {exc}")
        if dec < 0:
            raise ValueError("amount must be non-negative")
        # Normalize to two decimal places for currency-like behavior
        self._amount = dec.quantize(Decimal("0.01"))

    # due_day
    @property
    def due_day(self) -> int:
        return self._due_day

    @due_day.setter
    def due_day(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("due_day must be an Integer")
        self._due_day = value

    # is_fixed
    @property
    def is_fixed(self) -> bool:
        return self._is_fixed

    @is_fixed.setter
    def is_fixed(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("is_fixed must be a Boolean")
        self._is_fixed = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "amount": str(self.amount),
            "due_day": self.due_day,
            "is_fixed": self.is_fixed
        }

    def __repr__(self) -> str:
        return (
            f"Expense(name={self.name!r}, amount={self.amount!r}, due_date={self.due_day!r}, is_fixed={self.is_fixed}"
        )
