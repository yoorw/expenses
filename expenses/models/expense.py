from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Optional, Dict, Any


class Expense:
    """Represent a single expense item.

    Attributes
    - name: name of expense
    - amount: Decimal monetary amount (must be >= 0 and have at most 2 decimal places)
    - due_day: day of the month the expense is typically due 
    - is_fixed: True if expense MUST be paid (e.g., rent), False if optional (e.g., entertainment)
    """

    def __init__(
        self,
        name: str,
        amount: Decimal,
        due_day: int,
        is_fixed: bool,
    ) -> None:
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
        self._name = value

    # amount (store as Decimal)
    @property
    def amount(self) -> Decimal:
        return self._amount

    @amount.setter
    def amount(self, value: Decimal) -> None:
        # Ensure amount is always stored with exactly 2 decimal places
        if isinstance(value, Decimal):
            self._amount = value.quantize(Decimal("0.01"))
        else:
            # Convert to Decimal first, then quantize
            self._amount = Decimal(str(value)).quantize(Decimal("0.01"))

    # due_day
    @property
    def due_day(self) -> int:
        return self._due_day

    @due_day.setter
    def due_day(self, value: int) -> None:
        self._due_day = value

    # is_fixed
    @property
    def is_fixed(self) -> bool:
        return self._is_fixed

    @is_fixed.setter
    def is_fixed(self, value: bool) -> None:
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
