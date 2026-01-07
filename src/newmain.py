from decimal import Decimal

def is_field_valid(field: str) -> bool:
    """Check if the input field is valid (not empty)."""
    if not field or field == "":
        print(" Input cannot be empty. Please try again.")
        return False

    print(f"Expense name entered: {field}")
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

def main():
    expenses = []
    add_expenses = True 

    while add_expenses:
        # expense name
        name = request_field("Enter expense name: ")
        if name is None:
            break

        # expense amouunt
        amount = request_field("Enter expense amount: ")
        if amount is None:
            break

        if name and amount:
            expenses.append(
                {
                    "name": name,
                    "amount": Decimal(amount)
                }
            )

            print(f"Expense entered: {expenses[-1]}")

        add_expense_response = input("Do you want to add another expense? (yes/no): ").strip().lower()
        print(f"add_expense_response: {add_expense_response}")
        if add_expense_response in ["yes", "y"]:
            continue
        elif add_expense_response in ["no", "n"]:
            print(f"These are your expenses: \n {expenses}")
            print("Exiting input.")
            add_expenses = False
        elif is_quit(add_expense_response):
            add_expenses = False 
        else:
            print("Invalid Response. Exiting input.")
            break


            






if __name__ == "__main__":
    main()
