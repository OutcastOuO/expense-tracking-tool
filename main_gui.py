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
        self.root.geometry("1400x720")
        self.root.configure(background="#FDF5E6")
        
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
        self.top_frame = tk.Frame(self.root, background="#FDF5E6")
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.list_frame = tk.Frame(self.top_frame, background="#FDF5E6", width=400)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- 設定樣式 (Style) ---
        style = ttk.Style()
        style.theme_use("clam") 

        style.configure("Treeview", 
                        font=("Microsoft JhengHei", 13), 
                        rowheight=33,
                        background="#FFFDF5",
                        fieldbackground="#FFFDF5",
                        foreground="#4B3621")
        
        style.map("Treeview", background=[('selected', '#BC8F8F')])

        style.configure("Treeview.Heading", 
                        font=("Microsoft JhengHei", 16, "bold"),
                        rowheight=42,
                        background="#D2B48C", 
                        foreground="#4B3621",
                        relief="raised",
                        bordercolor="#FFFDF5",
                        lightcolor="#C9AB87",
                        darkcolor="#C9AB87",
                        padding=(0, 6))

        style.map("Treeview.Heading",
                  background=[('active', '#C1A37E')],
                  relief=[('active', 'raised'), ('pressed', 'sunken')])

        # --- 左側：Treeview 清單 ---
        columns = ("date", "name", "category", "amount")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')
        
        # 設定標籤顏色
        self.tree.tag_configure('oddrow', background="#FAF0E6")
        self.tree.tag_configure('evenrow', background='#FFFDF5')

        # 設定欄位屬性
        self.tree.column("date", width=80, anchor="center")
        self.tree.column("name", width=120, anchor="center")
        self.tree.column("category", width=40, anchor="center")
        self.tree.column("amount", width=100, anchor="e")
        
        # 定義欄位名稱
        self.tree.heading("date", text="日期")
        self.tree.heading("name", text="名稱")
        self.tree.heading("category", text="類別")
        self.tree.heading("amount", text="金額")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滾動條樣式
        scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- 右側：圓餅圖 ---
        self.chart_outer_frame = tk.Frame(self.top_frame, bg="#FDF5E6", padx=3, pady=3)
        self.chart_outer_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 裝飾性邊框
        self.chart_frame = tk.LabelFrame(self.chart_outer_frame,  
                                        font=("Microsoft JhengHei", 13, "bold"),
                                        fg="#4B3621",
                                        bg="#FFFDF5",
                                        relief="flat", 
                                        padx=5, pady=5)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # 建立圓餅圖
        self.fig, self.axis = plt.subplots(figsize=(4, 4), facecolor="#FFFDF5")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas_widget.configure(bg="#FFFDF5")

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
        for i, item in enumerate(data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, 
                            values=(item['date'], item['name'], item['category'], item['amount']),
                            tags=(tag,))
        
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