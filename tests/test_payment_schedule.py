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

    assert schedule.period_1_expenses == [expense1, expense2]
    assert schedule.period_2_expenses == [expense2, expense1]
    assert schedule.tolerance == Decimal("0.05")

def test_calculate_period_totals():
    expense1 = Expense(
        name="Rent",
        amount=Decimal("1200.00"),
        due_day=1,
        is_fixed=True
    )

    expense2 = Expense(
        name="Utilities",
        amount=Decimal("150.00"),
        due_day=15,
        is_fixed=False
    )

    expense3 = Expense(
        name="Cable",
        amount=Decimal("270.00"),
        due_day=15,
        is_fixed=False
    )

    schedule = PaymentSchedule(
        period_1_expenses=[expense1, expense2],
        period_2_expenses=[expense2, expense3],
        tolerance=Decimal("0.05")
    )

    schedule.period_1_total = schedule._calculate_period_total(schedule.period_1_expenses)
    assert schedule.period_1_total == Decimal("1350.00")

    schedule.period_2_total = schedule._calculate_period_total(schedule.period_2_expenses)
    assert schedule.period_2_total == Decimal("420.00")

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

    schedule.period_1_total = schedule._calculate_period_total(schedule.period_1_expenses)
    schedule.period_2_total = schedule._calculate_period_total(schedule.period_2_expenses)

    schedule.is_balanced = schedule._check_balance(schedule.period_1_total, schedule.period_2_total)

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
        tolerance=Decimal("2")
    )

    schedule.period_1_total = schedule._calculate_period_total(schedule.period_1_expenses)
    schedule.period_2_total = schedule._calculate_period_total(schedule.period_2_expenses)
    schedule.is_balanced = schedule._check_balance(schedule.period_1_total, schedule.period_2_total)

    assert schedule.is_balanced is False

