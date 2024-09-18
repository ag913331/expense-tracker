import argparse
import json
import sys

from pathlib import Path

DATA = "expenses.json"

def load_data():
    try:
        with open(DATA, "r") as file:
            tasks_data = json.load(file)
            return [task for task in tasks_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(e)

def save_data(expenses: list) -> bool:
    try:
        with open(DATA, "w") as file:
            json.dump(expenses, file, indent=4)
        return True
    except Exception as e:
        print(e)
        return False

def add_expense(description: str, amount: float):
    expenses = load_data()
    new_id = len(expenses) + 1
    expenses.append({"id": new_id, "description": description, "amount": amount})
    succeeded = save_data(expenses)

    if succeeded:
        print(f"Expense added successfully (ID: {new_id})")
    else:
        print("Action ADD EXPENSE failed")
    

def update_expense(id: int, description: str = None, amount: float = None):
    expenses = load_data()
    expense_to_update = next((expense for expense in expenses if expense["id"] == id), None)
    if expense_to_update is None:
        print(f"Expense with ID {id} not found.")
        return
    
    if description:
        expense_to_update["description"] = description
    
    if amount:
        expense_to_update["amount"] = amount

    save_data(expenses)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def validate_amount(amount: str):
    if not is_number(amount):
        return False, f"[ERR] Amount must be numeric. Expected number, got \"{amount}\""
    
    if float(amount) <= 0:
        return False, "[ERR] Expense amount must be greater than 0"
    
    return True, ""

def main() -> None:
    parser = argparse.ArgumentParser(description="Expense tracker CLI")
    subparsers = parser.add_subparsers(help="list of actions", dest="action", required=True)

    add_expense_parser = subparsers.add_parser("add", help="Add expense related arguments")
    add_expense_parser.add_argument("-d", "--description", type=str, required=True, help="Expense description")
    add_expense_parser.add_argument("-a", "--amount", type=str, required=True, help="Expense amount")

    update_expense_parser = subparsers.add_parser("update", help="Update expense related arguments")
    update_expense_parser.add_argument("--id", type=int, required=True, help="Expense ID")
    update_expense_parser.add_argument("-d", "--description", type=str, required=False, help="Expense description")
    update_expense_parser.add_argument("-a", "--amount", type=str, required=False, help="Expense amount")

    args = parser.parse_args()
    
    if args.action == "add":
        valid, message = validate_amount(args.amount)
        if not valid:
            print(message)
            sys.exit(-1)
        add_expense(args.description, float(args.amount))
    elif args.action == "update":
        if args.description or args.amount:
            valid, message = validate_amount(args.amount)
            if not valid:
                print(message)
                sys.exit(-1)
            update_expense(int(args.id), args.description, float(args.amount))
        else:
            print(f"Action UPDATE requires description or amount, or both.")
    # handle_task(args)

if __name__ == "__main__":
    main()