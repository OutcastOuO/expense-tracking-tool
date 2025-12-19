import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import data_storage
import chart_generator

# --- 記帳工具gui ---
class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("記帳工具")
        self.root.geometry("1200x720")

        # input
        input_frame = tk.Frame(root, padx=20, pady=20)
        input_frame.pack(side=tk.BOTTOM, fill=tk.Y)

        tk.Label(input_frame, text="金額:").pack()
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.pack()

        tk.Label(input_frame, text="類別:").pack()
        self.category_combo = ttk.Combobox(input_frame, values=["食", "衣", "住", "行", "樂"])
        self.category_combo.pack()

        btn = tk.Button(input_frame, text="儲存並更新圖表", command=self.handle_submit)
        btn.pack(pady=20)

        # 圖表
        self.setup_top_view()

        self.refresh_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # 上方主容器
    def setup_top_view(self):
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --- 左側：Treeview 清單 ---
        self.list_frame = tk.Frame(self.top_frame)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        columns = ("date", "name", "category", "amount")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')
        
        # 定義欄位名稱
        self.tree.heading("date", text="日期")
        self.tree.heading("name", text="名稱")
        self.tree.heading("category", text="類別")
        self.tree.heading("amount", text="金額")
        
        scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- 右側：圓餅圖 ---
        self.chart_frame = tk.Frame(self.top_frame, width=450)
        self.chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        self.fig, self.axis = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def handle_submit(self):
        # 取得資料
        amount = self.amount_entry.get()
        category = self.category_combo.get()
        
        if not amount or not category:
            messagebox.showwarning("錯誤", "請填寫完整資訊")
            return

        data_storage.save_expense({"amount": amount, "category": category})
        
        self.refresh_ui()
        self.amount_entry.delete(0, tk.END)

    def refresh_ui(self):
        # 清空舊清單
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 更新清單
        data = data_storage.load_all_expenses()
        for item in data:
            self.tree.insert("", tk.END, values=(item['date'], item['name'], item['category'], item['amount']))
        
        # 更新圓餅圖
        chart_generator.update_pie_chart(self.axis, data)
        self.canvas.draw()


    def on_close(self):
        """關閉視窗時清理資源並退出程式"""
        self.root.quit()       # 停止 mainloop
        self.root.destroy()    # 銷毀視窗，釋放 Tkinter 物件

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()