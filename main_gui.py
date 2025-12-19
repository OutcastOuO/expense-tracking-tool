import tkinter as tk
from tkinter import ttk, messagebox

import data_storage

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("記帳工具")
        self.root.geometry("1200x720")
        self.root.configure(background="#FDF5E6")

        style = ttk.Style()
        style.theme_use("clam")
        
        # input bar
        self.setup_input_bar()

    def setup_input_bar(self):
        # 欄容器
        self.bottom_bar = tk.Frame(self.root, pady=10, bg="#FDF5E6")
        self.bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 裝飾性分隔線
        separator = tk.Frame(self.bottom_bar, height=1, bg="#D2B48C")
        separator.pack(fill=tk.X, side=tk.TOP, pady=(0, 10))

        # 內部水平容器
        inner_container = tk.Frame(self.bottom_bar, bg="#FDF5E6")
        inner_container.pack(expand=True)

        # 統一文字與輸入框樣式
        lbl_font = ("Microsoft JhengHei", 12, "bold")
        lbl_color = "#4B3621"
        
        # Entry 的統一樣式
        entry_style = {
            "font": ("Microsoft JhengHei", 12),
            "relief": "flat",
            "highlightthickness": 1,
            "highlightbackground": "#D2B48C",
            "highlightcolor": "#8B4513"
        }

        # --- 名稱 ---
        tk.Label(inner_container, text="名稱", bg="#FDF5E6", fg=lbl_color, font=lbl_font).pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(inner_container, width=15, **entry_style)
        self.name_entry.pack(side=tk.LEFT, padx=2)

        # --- 類別 ---
        tk.Label(inner_container, text="類別", bg="#FDF5E6", fg=lbl_color, font=lbl_font).pack(side=tk.LEFT, padx=5)
        self.cat_combo = ttk.Combobox(inner_container, values=["食", "衣", "住", "行", "樂"], width=8, font=("Microsoft JhengHei", 11))
        self.cat_combo.pack(side=tk.LEFT, padx=2)

        # --- 花費 ---
        tk.Label(inner_container, text="花費", bg="#FDF5E6", fg=lbl_color, font=lbl_font).pack(side=tk.LEFT, padx=5)
        self.amount_entry = tk.Entry(inner_container, width=10, **entry_style)
        self.amount_entry.pack(side=tk.LEFT, padx=2)

        # --- 日期 ---
        tk.Label(inner_container, text="日期", bg="#FDF5E6", fg=lbl_color, font=lbl_font).pack(side=tk.LEFT, padx=5)
        self.date_entry = tk.Entry(inner_container, width=12, **entry_style)
        self.date_entry.insert(0, "2025-12-19") # 你的預設格式
        self.date_entry.pack(side=tk.LEFT, padx=10)

        # --- 新增按鈕 ---
        self.add_btn = tk.Button(inner_container, text=" ＋ 儲存 ", 
                                 command=self.handle_submit,
                                 bg="#A0522D", fg="white",
                                 font=("Microsoft JhengHei", 11, "bold"),
                                 relief="flat", padx=20, pady=3,
                                 activebackground="#8B4513", activeforeground="white",
                                 cursor="hand2")
        self.add_btn.pack(side=tk.LEFT, padx=20)

    def handle_submit(self):
        """收集數據並以字典格式存入 data_storage"""
        # 取得資料
        name = self.name_entry.get().strip()
        category = self.cat_combo.get().strip()
        amount = self.amount_entry.get().strip()
        date = self.date_entry.get().strip()

        # 驗證
        if not (name and category and amount and date):
            messagebox.showwarning("提示", "所有欄位都要填寫喔")
            return

        try:
            amount_val = float(amount)
        except ValueError:
            messagebox.showerror("錯誤", "花費請輸入數字喔")
            return

        # 封裝成字典
        expense_data = {
            "name": name,
            "category": category,
            "amount": amount_val,
            "date": date
        }

        # 執行儲存
        try:
            data_storage.save_expense(expense_data)
            
            self.name_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("儲存失敗", f"發生錯誤：{e}")    

    def refresh_ui(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()