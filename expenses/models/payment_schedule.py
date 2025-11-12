from decimal import Decimal

from expenses.models.expense import Expense

class PaymentSchedule:
    """Represent calculated output periods
    
    Attributes
    - period_1_total: total amount required for first pay period 
    - period_two_total: total amount required for second pay period
    - period_1_expenses: list of specific Expense objects assigned to Pay Period 1 
    - period_2_expenses: list of specific Expense objects assigned to Pay Period 2
    - is_balanced: True if final split is within an acceptable difference (e.g. less than 5% difference)
    """

    def __init__(
            self,
            period_1_total: Decimal,
            period_2_total: Decimal,
            period_1_expenses: list[Expense],
            period_2_expenses: list[Expense],
            acceptable_difference: Decimal
    ) -> None:
        self.period_1_total = period_1_total
        self.period_2_total = period_2_total
        self.period_1_expenses = period_1_expenses
        self.period_2_expenses = period_2_expenses
        self.acceptable_difference = acceptable_difference
        self.is_balanced = self._check_balance(self.acceptable_difference)

    def _check_balance(self) -> bool:
        """Check if the difference between periods is within acceptable range"""
        total = self.period_1_total + self.period_2_total
        if total == 0:
            return True  # No expenses, considered balanced
        difference = abs(self.period_1_total - self.period_2_total)
        difference_ratio = difference / total
        return difference_ratio <= self.acceptable_difference