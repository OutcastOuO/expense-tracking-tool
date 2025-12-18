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
        
        # input
        input_frame = tk.Frame(root, padx=20, pady=20)
        input_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(input_frame, text="金額:").pack()
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.pack()

        tk.Label(input_frame, text="類別:").pack()
        self.category_combo = ttk.Combobox(input_frame, values=["食", "衣", "住", "行", "樂"])
        self.category_combo.pack()

        btn = tk.Button(input_frame, text="儲存並更新圖表", command=self.handle_submit)
        btn.pack(pady=20)

        # 圖表
        self.fig, self.axis = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.refresh_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

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
        current_data = data_storage.load_all_expenses()
        chart_generator.update_pie_chart(self.axis, current_data)
        self.canvas.draw()

    def on_close(self):
        """關閉視窗時清理資源並退出程式"""
        self.root.quit()       # 停止 mainloop
        self.root.destroy()    # 銷毀視窗，釋放 Tkinter 物件

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()