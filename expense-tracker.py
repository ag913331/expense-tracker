import argparse
import json
import sys

from pathlib import Path
from datetime import datetime

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
    expenses.append(
        {
            "id": new_id, 
            "description": description, 
            "amount": amount,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    )
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
        expense_to_update["updated_at"] = datetime.now().isoformat()
    
    if amount:
        expense_to_update["amount"] = amount
        expense_to_update["updated_at"] = datetime.now().isoformat()

    save_data(expenses)

def delete_expense(id: int):
    expenses = load_data()
    
    expense_to_delete = next((expense for expense in expenses if expense["id"] == id))

    if expense_to_delete is None:
        print(f"Expense with ID {id} not found.")
        return
    
    expenses = [expense for expense in expenses if expense["id"] != id]
    save_data(expenses)

    print("Expense deleted successfully")

def list_expenses():
    expenses = load_data()

    for expense in expenses:
        dt = datetime.fromisoformat(expense['created_at'])
        formatted_date = dt.strftime('%Y-%m-%d')
        print(f"# {expense['id']}  {formatted_date}  {expense['description']}  {expense['amount']}")

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
    add_expense_parser.add_argument("-a", "--amount", type=float, required=True, help="Expense amount")

    update_expense_parser = subparsers.add_parser("update", help="Update expense related arguments")
    update_expense_parser.add_argument("--id", type=int, required=True, help="Expense ID")
    update_expense_parser.add_argument("-d", "--description", type=str, required=False, help="Expense description")
    update_expense_parser.add_argument("-a", "--amount", type=str, required=False, help="Expense amount")

    delete_expense_parser = subparsers.add_parser("delete", help="Delete expense related arguments")
    delete_expense_parser.add_argument("--id", type=int, required=True, help="Expense ID")

    subparsers.add_parser("list", help="Delete expense related arguments")

    args = parser.parse_args()
    
    if args.action == "add":
        valid, message = validate_amount(args.amount)
        if not valid:
            print(message)
        add_expense(args.description, args.amount)
    elif args.action == "update":
        if args.description or args.amount:
            valid, message = validate_amount(args.amount)
            if not valid:
                print(message)
                sys.exit(-1)
            update_expense(int(args.id), args.description, float(args.amount))
        else:
            print(f"Action UPDATE requires description or amount, or both.")
    elif args.action == "delete":
        delete_expense(int(args.id))
    elif args.action == "list":
        list_expenses()

if __name__ == "__main__":
    main()