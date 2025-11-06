from expense import Expense

exp = Expense("Internet Bill", 59.99, due_day=15, is_fixed=True)
print(exp)
print(exp.amount)
print(exp.to_dict())