import json
import os

DB_FILE = 'expenses.json'

def save_expense(date, name, category, amount):
    data = load_all_expenses()
    new_item = {
        "date": date,
        "name": name,
        "category": category,
        "amount": amount,
        
    }
    data.append(new_item)
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_all_expenses():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []
def delete_expense(index):
    """讀取資料，刪除指定位置的項目，重新存檔"""
    data = load_all_expenses()
    if 0 <= index < len(data):
        data.pop(index)  # 移除該索引的資料
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    return False