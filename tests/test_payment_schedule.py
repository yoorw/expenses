from decimal import Decimal
import pytest

from expenses.models.expense import Expense
from expenses.models.payment_schedule import PaymentSchedule

def test_basic_construction():
    expense1 = Expense(
        name="Rent",
        amount=Decimal("1200.00"),
        due_day=1,
        is_fixed=True
    )
    print(f"[test_basic] expense 1 has amount: {expense1.amount} and type is: {type(expense1.amount)}")

    expense2 = Expense(
        name="Utilities",
        amount=Decimal("150.00"),
        due_day=15,
        is_fixed=False
    )

    schedule = PaymentSchedule(
        period_1_expenses=[expense1, expense2],
        period_2_expenses=[expense2, expense1],
        tolerance=Decimal("0.05")
    )


    # assert schedule.period_1_total == Decimal("600.00")
    # assert schedule.period_2_total == Decimal("750.00")
    assert schedule.period_1_expenses == [expense1, expense2]
    assert schedule.period_2_expenses == [expense2, expense1]
    assert schedule.tolerance == Decimal("0.05")
    # assert schedule.is_balanced is False

def test_periods_balanced():
    expense1 = Expense(
        name="Subscription",
        amount=Decimal("52.00"),
        due_day=10,
        is_fixed=True
    )
    expense2 = Expense(
        name="Groceries",
        amount=Decimal("53.00"),
        due_day=20,
        is_fixed=False
    )

    schedule = PaymentSchedule(
        period_1_expenses=[expense1],
        period_2_expenses=[expense2],
        tolerance=Decimal("2")
    )

    assert schedule.is_balanced is True    

def test_periods_not_balanced():
    expense1 = Expense(
        name="Subscription",
        amount=Decimal("50.00"),
        due_day=10,
        is_fixed=True
    )
    expense2 = Expense(
        name="Groceries",
        amount=Decimal("55.00"),
        due_day=20,
        is_fixed=False
    )

    schedule = PaymentSchedule(
        period_1_expenses=[expense1],
        period_2_expenses=[expense2],
        acceptable_difference=Decimal("0.10")
    )

    assert schedule.is_balanced is False

