import json
from decimal import Decimal, ROUND_HALF_UP

from utils.decimalencoder import DecimalEncoder

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

def calculate_payment_amounts(expenses: list[dict]) -> list[dict]:
    """Calculate payment amounts based on expenses (not implemented)."""
    # Placeholder implementation
    payment_plan = []

    total_expense = sum(expense['amount'] for expense in expenses)
    half_expense = (total_expense / 2).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        



        


    return payment_plan

def schedule_payments(payment_plan: list[dict]) -> None:
    """Schedule payments based on the payment plan (not implemented)."""
    # Placeholder implementation
    pass



def main():
    expenses = create_expenses()
    payment_plan = calculate_payment_amounts(expenses)
    schedule_payments(payment_plan)



if __name__ == "__main__":
    main()
