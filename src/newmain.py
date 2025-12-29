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

def main():
    # expense name
    valid_field = True 

    while valid_field:
        name = input("Enter expense name: ").strip()

        if is_quit(name):           # check for quit command first 
            valid_field = False 

        elif is_field_valid(name):
            valid_field = False 




if __name__ == "__main__":
    main()
