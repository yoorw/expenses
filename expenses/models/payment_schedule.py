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
            period_1_expenses: list[Expense],
            period_2_expenses: list[Expense],
            tolerance: Decimal
    ) -> None:
        self.period_1_expenses = period_1_expenses
        self.period_2_expenses = period_2_expenses
        self.tolerance = tolerance
        # self.period_1_total = self._calculate_period_total(self.period_1_expenses),
        # self.period_2_total = self._calculate_period_total(self.period_2_expenses),
        # self.is_balanced = self._check_balance()
        self.period_1_total = None,
        self.period_2_total = None,
        self.is_balanced = None

    def _calculate_period_total(self, expenses: list[Expense]) -> Decimal:
        """Calculate total amount for a list of expenses"""
        total = Decimal("0.00")
        for expense in expenses:
            print(f"[_calculate_period_total] total: {total} with type: {type(total)}")
            print(f"[_calculate_period_total] expense.amount: {expense.amount} with type: {type(expense.amount)}")
            print(f"[_calculate_period_total] EXPECTED total calculation: {total + expense.amount} with type: {type(total + expense.amount)}")
            total += expense.amount

        # print(f"[_calculate_period_total] total.quantize: {total.quantize(Decimal('0.01'))}")
        # return total.quantize(Decimal("0.01"))
        return total
    
    def _check_balance(self) -> bool:
        """Check if the difference between periods is within acceptable range"""
        self.period_1_total = self._calculate_period_total(self.period_1_expenses),
        self.period_2_total = self._calculate_period_total(self.period_2_expenses),
        print(f"[_check_balance] period 1 total: {self.period_1_total} and type: {type(self.period_1_total)}")
        print(f"[_check_balance] period 2 total: {self.period_2_total} and type: {type(self.period_2_total)}")
        total = self.period_1_total + self.period_2_total
        print(f"[_check_balance] TOTAL: {total} and type is: {type(total)}")
        if total == 0:
            return True  # No expenses, considered balanced
        difference = abs(self.period_1_total - self.period_2_total)
        acceptable_difference = (total / 2) * (self.tolerance / 100)

        self.is_balanced = False

        if difference <= acceptable_difference:
            self.is_balanced = True
        
    