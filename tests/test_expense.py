from datetime import date
from decimal import Decimal
import pytest 

from expenses.models.expense import Expense

def test_basic_contruction():
    expense = Expense(
        name="Lunch",
        amount=12.5,
        due_day=15,
        is_fixed=True
    )

    assert expense.title == "Lunch"
# class TestExpense(unittest.TestCase):
#     def test_basic_construction(self):
#         e = Expense("Comcast", 165.00, due_day=10, is_fixed=False)
#         self.assertEqual(e.name, "Comcast")
#         self.assertEqual(e.amount, Decimal("165.00"))
#         self.assertEqual(e.due_day, 10)
#         self.assertEqual(e.is_fixed, False)

#     def test_amount_validation(self):
#         with self.assertRaises(ValueError):
#             Expense("Bad", "not-a-number", 10, True)

#         with self.assertRaises(ValueError):
#             Expense("Negative", -5, 10, False)

#     def test_to_dict(self):
#         e = Expense("North Shore Gas", "89.50", 7, True)
#         d = e.to_dict()
#         self.assertIn("name", d)
#         self.assertIn("amount", d)
#         self.assertEqual(d["name"], "North Shore Gas")


# if __name__ == "__main__":
#     unittest.main()
