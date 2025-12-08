from expenses.models.expense import Expense

exp = Expense("Internet Bill", 59.99, due_day=15, enforce_due_day=True)
print(exp)
print(exp.amount)
print(exp.to_dict())