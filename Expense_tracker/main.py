"""Simple Expense Tracker - runs in the terminal, no installs needed.
Run:  python main.py
"""
import json
import os
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.json")


def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses):
    title = input("What did you spend on? ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    category = input("Category (food/travel/study/other): ").strip().lower() or "other"
    expenses.append({"title": title, "amount": amount,
                     "category": category, "date": str(date.today())})
    save(expenses)
    print("Expense added!")


def show_all(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    print(f"\n{'#':<4}{'Date':<12}{'Title':<20}{'Category':<10}{'Amount':>8}")
    print("-" * 54)
    for i, e in enumerate(expenses, 1):
        print(f"{i:<4}{e['date']:<12}{e['title']:<20}{e['category']:<10}{e['amount']:>8.2f}")
    print("-" * 54)
    print(f"{'Total':<46}{sum(e['amount'] for e in expenses):>8.2f}")


def summary(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    print("\nSpending by category:")
    for cat, amt in sorted(totals.items(), key=lambda x: -x[1]):
        print(f"  {cat:<10} {amt:>8.2f}")


def delete_expense(expenses):
    show_all(expenses)
    if not expenses:
        return
    try:
        n = int(input("Number to delete: "))
        removed = expenses.pop(n - 1)
        save(expenses)
        print(f"Deleted: {removed['title']}")
    except (ValueError, IndexError):
        print("Invalid number.")


def main():
    expenses = load()
    menu = """
=== Expense Tracker ===
1. Add expense
2. View all expenses
3. Summary by category
4. Delete an expense
5. Exit
"""
    while True:
        print(menu)
        choice = input("Choose (1-5): ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_all(expenses)
        elif choice == "3":
            summary(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
