from __future__ import annotations

from dataclasses import dataclass
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
        title: str,
        amount: Any,
        *,
        currency: str = "USD",
        date_: Optional[date] = None,
        category: Optional[str] = None,
        notes: Optional[str] = None,
        paid: bool = False,
        id: Optional[str] = None,
    ) -> None:
        # Basic validation and assignments
        self._id = id
        self.title = title
        self.amount = amount
        self.currency = currency
        self.date = date_ or date.today()
        self.category = category
        self.notes = notes
        self.paid = paid

    # id property (optional)
    @property
    def id(self) -> Optional[str]:
        return self._id

    @id.setter
    def id(self, value: Optional[str]) -> None:
        self._id = value

    # title
    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("title must be a non-empty string")
        self._title = value.strip()

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

    # currency
    @property
    def currency(self) -> str:
        return self._currency

    @currency.setter
    def currency(self, value: str) -> None:
        if not isinstance(value, str) or not value:
            raise ValueError("currency must be a non-empty string")
        self._currency = value.upper()

    # date
    @property
    def date(self) -> date:
        return self._date

    @date.setter
    def date(self, value: Optional[date]) -> None:
        if value is None:
            self._date = date.today()
            return
        if isinstance(value, datetime):
            value = value.date()
        if not isinstance(value, date):
            raise ValueError("date must be a datetime.date (or datetime)")
        self._date = value

    # category
    @property
    def category(self) -> Optional[str]:
        return self._category

    @category.setter
    def category(self, value: Optional[str]) -> None:
        self._category = value.strip() if isinstance(value, str) and value.strip() else None

    # notes
    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @notes.setter
    def notes(self, value: Optional[str]) -> None:
        self._notes = value.strip() if isinstance(value, str) and value.strip() else None

    # paid
    @property
    def paid(self) -> bool:
        return self._paid

    @paid.setter
    def paid(self, value: bool) -> None:
        self._paid = bool(value)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "amount": str(self.amount),
            "currency": self.currency,
            "date": self.date.isoformat(),
            "category": self.category,
            "notes": self.notes,
            "paid": self.paid,
        }

    def __repr__(self) -> str:
        return (
            f"Expense(title={self.title!r}, amount={self.amount!r}, currency={self.currency!r}, "
            f"date={self.date!r}, category={self.category!r}, paid={self.paid!r})"
        )
