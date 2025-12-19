import json
import os

DB_FILE = 'expenses.json'

def save_expense(name, category, amount, date):
    data = load_all_expenses()
    new_item = {
        "name": name,
        "category": category,
        "amount": amount,
        "date": date
    }
    data.append(new_item)
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_all_expenses():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []