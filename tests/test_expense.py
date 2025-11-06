import unittest
from datetime import date
from decimal import Decimal

from expense import Expense


class TestExpense(unittest.TestCase):
    def test_basic_construction(self):
        e = Expense("Comcast", 165.00, due_day=10, is_fixed=False)
        self.assertEqual(e.name, "Comcast")
        self.assertEqual(e.amount, Decimal("165.00"))
        self.assertEqual(e.due_day, 10)
        self.assertEqual(e.is_fixed, False)

    def test_amount_validation(self):
        with self.assertRaises(ValueError):
            Expense("Bad", "not-a-number")

        with self.assertRaises(ValueError):
            Expense("Negative", -5)

    def test_to_dict(self):
        e = Expense("North Shore Gas", "89.50")
        d = e.to_dict()
        self.assertIn("namee", d)
        self.assertIn("amount", d)
        self.assertEqual(d["name"], "North Shore Gas")


if __name__ == "__main__":
    unittest.main()
