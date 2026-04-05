import json
from decimal import Decimal, ROUND_HALF_UP

from src.utils.decimalencoder import DecimalEncoder
from src.utils.utils import decimal_to_currency


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
                "amount": amount,
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
            print("\nThese are your expenses:\n")

            for expense in expenses:
                print(f"  - {expense['name']}: ${expense['amount']:,.2f}")

            print("\nSaving expenses...")
            # save_expenses(expenses)       #TODO: improve logic to save expenses

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

    save_expenses = request_field("Do you want to save the Expenses as a file? (yes/no):")

    if save_expenses in ["yes", "y"]:
        file_name = request_field("Enter the name of the expenses file to save (e.g., expenses.json): ")
        file_path = request_field("Enter full path directory to save the expenses file (e.g., /path/to/): ")
        file_dir = file_path + file_name
        with open(file_dir, 'w') as f:
            json.dump(expenses, f, cls=DecimalEncoder, indent=4)

        print(f"Expenses saved to {file_dir}.")

def calculate_payment_plan(expenses: list[dict]) -> tuple[list[dict], list[dict]]:
    # filter out split expenses 
    nonsplit_expenses = [expense for expense in expenses if expense['is_split'].lower() in ['no', 'n']]
    split_expenses = [expense for expense in expenses if expense['is_split'].lower() in ['yes', 'y']]

    print(f"nonsplit_expenses: {nonsplit_expenses}")
    print(f"split_expenses: {split_expenses}")

    expenses_1, expenses_2 = calculate_payment_split(nonsplit_expenses)

    # add back in expenses that can be split
    expenses_1 = expenses_1 + split_expenses
    expenses_2 = expenses_2 + split_expenses 

    return expenses_1, expenses_2


def calculate_payment_split(expenses: list[dict]) -> tuple[list[dict], list[dict]]:
    """Calculate payment amounts based on expenses. Uses Partition Backtracking Algorithm"""

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


def print_payment_plan(subset_1: list[dict], subset_2: list[dict]) -> None:
    """Create a payment plan based on the expenses (not implemented)."""
    totals = []
    for idx, expenses in enumerate([subset_1, subset_2]):
        total = sum(expense['amount'] if expense['is_split'] in ['no', 'n'] else (expense['amount']/2) for expense in expenses)
        totals.append(total)

        print(f"\nPayment Schedule {idx+1}:")
        total_formatted = decimal_to_currency(total)
        print(f"Total Amount: ${total_formatted:,.2f}")
        print("Expenses:")
        for expense in expenses:
            print("-"*20)
            for expense_field, expense_val in expense.items():
                # convert amount field to string format
                if expense_field == "amount":
                    expense_val = f"${total_formatted:,.2f}"

                print(f" - {expense_field}: {expense_val}")

            # if the expense can be split, show split amount
            if expense['is_split'] in ['yes', 'y']:
                split_val = expense['amount'] / 2
                print(f"   -> Split Amount for {expense['name']}: ${split_val:,.2f}")


    expense_diff = abs(totals[0] - totals[1])
    print(f"\nDifference between schedules: ${decimal_to_currency(expense_diff):,.2f}\n")


def schedule_payments(payment_plan_1: list[dict], payment_plan_2: list[dict]) -> None:
    """Schedule payments based on the payment plan (not implemented)."""
    # Placeholder implementation
    pass


def main():
    expenses = create_expenses()
    subset_1, subset_2 = calculate_payment_plan(expenses)
    print_payment_plan(subset_1, subset_2)
    # schedule_payments(schedule_1, schedule_2)



if __name__ == "__main__":
    main()
