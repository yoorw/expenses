import unittest
from datetime import date
from decimal import Decimal

from expense import Expense


class TestExpense(unittest.TestCase):
    def test_basic_construction(self):
        e = Expense("Lunch", 12.5, currency="USD", date_=date(2025, 11, 3), category="meals", notes="team lunch", paid=True)
        self.assertEqual(e.title, "Lunch")
        self.assertEqual(e.amount, Decimal("12.50"))
        self.assertEqual(e.currency, "USD")
        self.assertEqual(e.date, date(2025, 11, 3))
        self.assertEqual(e.category, "meals")
        self.assertEqual(e.notes, "team lunch")
        self.assertTrue(e.paid)

    def test_amount_validation(self):
        with self.assertRaises(ValueError):
            Expense("Bad", "not-a-number")

        with self.assertRaises(ValueError):
            Expense("Negative", -5)

    def test_to_dict(self):
        e = Expense("Coffee", "2.3")
        d = e.to_dict()
        self.assertIn("title", d)
        self.assertIn("amount", d)
        self.assertEqual(d["title"], "Coffee")


if __name__ == "__main__":
    unittest.main()
