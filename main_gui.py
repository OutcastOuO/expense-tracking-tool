import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import data_storage

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("記帳工具")
        
        input_frame = tk.Frame(root, padx=20, pady=20)
        input_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(input_frame, text="金額:").pack()
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.pack()

        tk.Label(input_frame, text="類別:").pack()
        self.cat_combo = ttk.Combobox(input_frame, values=["食", "衣", "住", "行", "樂"])
        self.cat_combo.pack()

        btn = tk.Button(input_frame, text="儲存並更新圖表", command=self.handle_submit)
        btn.pack(pady=20)

        self.refresh_ui()

    def handle_submit(self):
        # 1. 取得資料
        amt = self.amount_entry.get()
        cat = self.cat_combo.get()
        
        if not amt or not cat:
            messagebox.showwarning("錯誤", "請填寫完整資訊")
            return

        data_storage.save_expense({"amount": amt, "category": cat})
        
        self.refresh_ui()
        self.amount_entry.delete(0, tk.END)
    
    def refresh_ui(self):
        current_data = data_storage.load_all_expenses()
        
     

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()