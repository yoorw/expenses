from decimal import Decimal
from expenses.models.expense import Expense


def get_valid_input(prompt: str, input_type=str, allow_empty=False):
    """Prompt for input and validate the type."""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and allow_empty:
                return None
            if not user_input:
                print("  ✗ Input cannot be empty. Please try again.")
                continue
            
            if input_type == int:
                value = int(user_input)
                if value < 1 or value > 31:
                    print("  ✗ Due day must be between 1 and 31.")
                    continue
                return value
            elif input_type == float:
                value = float(user_input)
                if value < 0:
                    print("  ✗ Amount must be non-negative.")
                    continue
                return value
            elif input_type == bool:
                if user_input.lower() in ("yes", "y", "true", "1"):
                    return True
                elif user_input.lower() in ("no", "n", "false", "0"):
                    return False
                else:
                    print("  ✗ Please enter 'yes' or 'no'.")
                    continue
            else:
                return user_input
        except ValueError as e:
            print(f"  ✗ Invalid input: {e}. Please try again.")


def add_expense():
    """Interactively add a single expense."""
    print("\n" + "=" * 60)
    print("ADD NEW EXPENSE")
    print("=" * 60)
    
    name = get_valid_input("  Expense name: ")
    amount = get_valid_input("  Amount ($): ", input_type=float)
    due_day = get_valid_input("  Due day (1-31): ", input_type=int)
    is_fixed = get_valid_input("  Is this a fixed expense? (yes/no): ", input_type=bool)
    
    try:
        expense = Expense(
            name=name,
            amount=amount,
            due_day=due_day,
            is_fixed=is_fixed,
        )
        print(f"  ✓ Expense '{name}' created successfully!")
        return expense
    except ValueError as e:
        print(f"  ✗ Error creating expense: {e}")
        return None


def display_expenses(expenses):
    """Display all expenses in a formatted table."""
    if not expenses:
        print("\n  No expenses to display.")
        return
    
    print("\n" + "=" * 60)
    print("EXPENSE LIST")
    print("=" * 60)
    
    for i, expense in enumerate(expenses, start=1):
        print(f"\n  [{i}] {expense.name}")
        print(f"      Amount: ${expense.amount}")
        print(f"      Due Day: {expense.due_day}")
        print(f"      Fixed: {'Yes' if expense.is_fixed else 'No'}")
    
    # Print summary
    print("\n" + "-" * 60)
    total = sum(exp.amount for exp in expenses)
    fixed_count = sum(1 for exp in expenses if exp.is_fixed)
    variable_count = len(expenses) - fixed_count
    
    print(f"  Total Expenses: {len(expenses)}")
    print(f"    - Fixed: {fixed_count}")
    print(f"    - Variable: {variable_count}")
    print(f"  Total Amount: ${total}")
    print("=" * 60)


def export_expenses(expenses):
    """Export expenses as a formatted list."""
    print("\n" + "=" * 60)
    print("EXPENSE DATA (as dictionaries)")
    print("=" * 60)
    
    for i, expense in enumerate(expenses, start=1):
        print(f"\n  [{i}] {expense.to_dict()}")
    print()


def main():
    """Main console application loop."""
    expenses = []
    
    print("\n" + "=" * 60)
    print("EXPENSE MANAGER")
    print("=" * 60)
    
    while True:
        print("\nOptions:")
        print("  1. Add an expense")
        print("  2. View all expenses")
        print("  3. Export expenses as data")
        print("  4. Exit")
        
        choice = get_valid_input("\nSelect an option (1-4): ")
        
        if choice == "1":
            expense = add_expense()
            if expense:
                expenses.append(expense)
        elif choice == "2":
            display_expenses(expenses)
        elif choice == "3":
            export_expenses(expenses)
        elif choice == "4":
            print("\n  ✓ Goodbye!")
            break
        else:
            print("  ✗ Invalid option. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()