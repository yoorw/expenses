import json
from decimal import Decimal, ROUND_HALF_UP

from utils.decimalencoder import DecimalEncoder
from utils.utils import decimal_to_currency

def is_field_valid(field: str) -> bool:
    """Check if the input field is valid (not empty)."""
    if not field or field == "":
        print(" Input cannot be empty. Please try again.")
        return False

    print(f"Expense value entered: {field}")
    return True

def is_quit(field: str) -> bool:
    """Check if the input field is 'quit'."""
    if field.lower() == "quit" or field.lower() == "q":
        print(" Exiting input.")
        return True
    return False

def request_field(input_prompt: str) -> str | None:
    valid_field = False 

    while not valid_field:
        field = input(input_prompt).strip()

        if is_quit(field):           # check for quit command first 
            # break
            return None

        elif is_field_valid(field):
            # valid_field = True
            return field
        
def create_expense() -> dict | None:        #TODO: return Expense object 
        # expense name
        name = request_field("Enter expense name: ")
        if name is None:
            return None

        # expense amouunt
        amount = request_field("Enter expense amount: ")
        if amount is None:
            return None

        # due_date
        due_date = request_field("Enter expense due date (1-31): ")
        if due_date is None:
            return None

        # fixed_due_date 
        fixed_due_date = request_field("Is the Expense Due Date a fixed date every month? (yes/no): ")
        if fixed_due_date is None:
            return None

        is_split = request_field("Can the payment be split (2 payments per month)? (yes/no): ")
        if is_split is None:
            return None
        
        is_active = request_field("Is the expense an active, on-going expense? (yes/no): ")
        if is_active is None:
            return None
        
        if name and amount and due_date and fixed_due_date and is_active:
            expense = {
                "name": name,
                "amount": Decimal(amount),
                "due_date": due_date,
                "fixed_due_date": fixed_due_date,
                "is_split": is_split,
                "is_active": is_active
            }

            print(f"Expense entered: {expense}")

            return expense 
        
def create_expenses() -> list[dict]: 
    expenses = []
    add_expenses = True 

    while add_expenses:

        expense = create_expense()

        if expense:
            expenses.append(expense)
        else:
            print("Expense not created.")


        add_expense_response = input("Do you want to add another expense? (yes/no): ").strip().lower()
        print(f"add_expense_response: {add_expense_response}")
        if add_expense_response in ["yes", "y"]:
            continue
        elif add_expense_response in ["no", "n"]:
            # print(f"\nThese are your expenses: \n {expenses}")
            print("\nThese are your expenses:\n")

            for expense in expenses:
                amount_formatted = expense['amount'].quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                print(f"  - {expense['name']}: ${amount_formatted:,.2f}")

            print("\nSaving expenses...")
            save_expenses(expenses)

            print("\nExiting input.")


            add_expenses = False

            return expenses

        elif is_quit(add_expense_response):
            add_expenses = False 
        else:
            print("Invalid Response. Exiting input.")
            break

def save_expenses(expenses: list) -> None:
    """Save expenses to a file or database (not implemented)."""
    # file_path = "/Volumes/swdev/swdev_docs/expenses/expenses.json"
    file_name = request_field("Enter the name of the expenses file to save (e.g., expenses.json): ")
    file_path = request_field("Enter full path directory to save the expenses file (e.g., /path/to/): ")
    file_dir = file_path + file_name
    with open(file_dir, 'w') as f:
        json.dump(expenses, f, cls=DecimalEncoder, indent=4)

    print(f"Expenses saved to {file_dir}.")

def calculate_payment_split(expenses: list[dict]) -> tuple[list[dict], list[dict]]:
    """Calculate payment amounts based on expenses. Uses Partition Backtracking Algorithm"""
    # Placeholder implementation
    payment_plan = []

    total_expense = sum(expense['amount'] for expense in expenses)
    target = total_expense / 2

    best_subset = []
    best_diff = float('inf')

    def backtrack(index: int, current_subset: list[dict], current_sum: Decimal):
        nonlocal best_subset, best_diff

        # best case: all expenses considered 
        if index == len(expenses):
            diff = abs(target - current_sum)
            if diff < best_diff:
                best_diff = diff
                best_subset = list(current_subset)

            return 
        
        # Choice 1: Include the current expense in Subset 1
        current_subset.append(expenses[index])
        backtrack(index + 1, current_subset, current_sum + expenses[index]['amount'])
        current_subset.pop() # Undo choice (backtrack)

        # Choice 2: Exclude current expense from Subset 1
        backtrack(index + 1, current_subset, current_sum)

    # Start recursion
    backtrack(0, [], 0)

    # Organize results into payment plans
    subset_1 = best_subset 
    subset_2 = list(expenses)
    for expense in subset_1:
        # Remove one expense from subset_2
        if expense in subset_2:
            subset_2.remove(expense)

    return subset_1, subset_2


def create_payment_plan(expenses: list[dict]) -> tuple[list[dict], list[dict]]:
    """Create a payment plan based on the expenses (not implemented)."""
    subset_1, subset_2 = calculate_payment_split(expenses)
    # confirm payment plan by outputting a breakdown of the 2 schedules and the expenses (name / amount) of each schedule and the difference 
    # subset_1 total amount
    total_1 = sum(expense['amount'] for expense in subset_1)
    total_2 = sum(expense['amount'] for expense in subset_2)

    expense_diff = abs(total_1 - total_2)

    print("\nPayment Schedule 1:")
    total_1_formatted = decimal_to_currency(total_1)
    print(f"Total Amount: ${total_1_formatted:,.2f}")
    print("Expenses:")
    for expense in subset_1:
        for expense_field, expense_value in expense.items():
            if expense_field == "amount":
                expense_value = decimal_to_currency(expense_value)

            print(f"  - {expense_field}: {expense_value}")

    print("\nPayment Schedule 2:")
    total_2_formatted = decimal_to_currency(total_2)
    print(f"Total Amount: ${total_2_formatted:,.2f}")
    print("Expenses:")
    for expense in subset_2:
        for expense_field, expense_value in expense.items():
            if expense_field == "amount":
                expense_value = decimal_to_currency(expense_value)

            print(f"  - {expense_field}: {expense_value}")

    print(f"\nDifference between schedules: ${decimal_to_currency(expense_diff):,.2f}\n")



def schedule_payments(payment_plan: list[dict]) -> None:
    """Schedule payments based on the payment plan (not implemented)."""
    # Placeholder implementation
    pass



def main():
    expenses = create_expenses()
    schedule_1, schedule_2 = create_payment_plan(expenses)
    schedule_payments(schedule_1, schedule_2)



if __name__ == "__main__":
    main()
