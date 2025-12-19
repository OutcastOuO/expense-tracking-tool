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

        self.setup_input_bar()

    def setup_input_bar(self):

        # 建立一個底欄容器
        self.bottom_bar = tk.Frame(self.root, pady=10, bg="#f0f0f0", bd=1, relief=tk.SUNKEN)
        self.bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 橫向排列輸入組件
        tk.Label(self.bottom_bar, text="名稱:").pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(self.bottom_bar, width=15)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.bottom_bar, text="類別:").pack(side=tk.LEFT, padx=5)
        self.cat_combo = ttk.Combobox(self.bottom_bar, values=["食", "衣", "住", "行", "樂"], width=10)
        self.cat_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(self.bottom_bar, text="花費:").pack(side=tk.LEFT, padx=5)
        self.amount_entry = tk.Entry(self.bottom_bar, width=10)
        self.amount_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.bottom_bar, text="日期:").pack(side=tk.LEFT, padx=5)
        self.date_entry = tk.Entry(self.bottom_bar, width=12)
        self.date_entry.insert(0, "2025-12-19") # 預設提示格式
        self.date_entry.pack(side=tk.LEFT, padx=5)

        self.add_btn = tk.Button(self.bottom_bar, text="新增", command=self.handle_submit)
        self.add_btn.pack(side=tk.LEFT, padx=10)    



    def handle_submit(self):
        # 1. 取得資料
        amount = self.amount_entry.get()
        category = self.cat_combo.get()
        name = self.name_entry.get()
        date = self.date_entry.get()

        # 2. 驗證
        if not (name and category and amount and date):
            messagebox.showwarning("提示", "所有欄位都必須填寫！")
            return


        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("錯誤", "金額請輸入數字！")
            return

        # 3. 儲存
        try:
            data_storage.save_expense(name, category, amount, date)
            
            # --- 成功提示 ---
            messagebox.showinfo("成功", f"已成功儲存：{name} ${amount}")

            # 清理輸入框
            self.name_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.refresh_ui()
            
        except Exception as e:
            messagebox.showerror("儲存失敗", f"發生錯誤：{e}")    

        
    def refresh_ui(self):
        current_data = data_storage.load_all_expenses()

       

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()