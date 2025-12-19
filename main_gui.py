import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import data_storage
import chart_generator

# --- 記帳工具 GUI ---
class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("記帳工具")
        self.root.geometry("1400x720")
        self.root.configure(background="#FFF8EE")

        style = ttk.Style()
        style.theme_use("clam")

        # --- 修改 Combobox 樣式 ---
        # 基本樣式
        style.configure("TCombobox", 
                        fieldbackground="#FFFFFF",
                        background="#D2B48C",     
                        foreground="#4B3621",     
                        darkcolor="#D2B48C",      
                        lightcolor="#D2B48C",     
                        selectbackground="#FFFFFF",
                        selectforeground="#4B3621")

        # readonly 狀態
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#FFF9F0")],
                  foreground=[("readonly", "#4B3621")],
                  selectbackground=[("readonly", "#FFF9F0")], 
                  selectforeground=[("readonly", "#4B3621")])
        
        # input
        self.setup_input_bar()

        # 圖表
        self.setup_top_view()

        self.refresh_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # 上方主容器
    def setup_top_view(self):
        self.top_frame = tk.Frame(self.root, background="#FDF5E6")
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.list_frame = tk.Frame(self.top_frame, background="#FDF5E6", borderwidth=0, highlightthickness=0)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- 設定樣式 (Style) ---
        style = ttk.Style()
        style.theme_use("clam") 

        style.configure("Treeview", 
                        font=("Microsoft JhengHei", 13), 
                        rowheight=33,
                        background="#FFFDF5",
                        fieldbackground="#FFFDF5",
                        foreground="#4B3621",
                        relief="flat")
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

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

        # --- Scrollbar 樣式優化 ---
        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background="#D2B48C",
                        troughcolor="#FDF5E6",
                        bordercolor="#FDF5E6",
                        lightcolor="#DBC4A7",
                        darkcolor="#DBC4A7",
                        borderwidth=0,
                        arrowsize=12)

        # 滑鼠滑過滑塊時變色
        style.map("Vertical.TScrollbar",
                  background=[('active', '#BC8F8F')],
                  arrowcolor=[('active', '#4B3621')])

        # --- 左側：Treeview 清單 ---
        columns = ("date", "name", "category", "amount")
        self.tree = ttk.Treeview(self.list_frame, 
                                columns=columns, 
                                show='headings', 
                                style="Treeview")
        
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
        self.chart_outer_frame = tk.Frame(self.top_frame, bg="#FDF5E6", padx=0, pady=0)
        self.chart_outer_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 裝飾性邊框
        self.chart_frame = tk.LabelFrame(self.chart_outer_frame,  
                                        font=("Microsoft JhengHei", 13, "bold"),
                                        fg="#4B3621",
                                        bg="#FFF8EE",
                                        relief="flat", 
                                        padx=2, pady=2)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # 建立圓餅圖
        self.fig, self.axis = plt.subplots(figsize=(4, 4), facecolor="#FFF8EE")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas_widget.configure(bg="#FFFDF5")

    def setup_input_bar(self):
        # 欄容器
        self.bottom_bar = tk.Frame(self.root, pady=5, bg="#FDF5E6")
        self.bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 裝飾性分隔線
        separator = tk.Frame(self.bottom_bar, height=3, bg="#D2B48C")
        separator.pack(fill=tk.X, side=tk.TOP, pady=(0, 5))

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
            "background": "#FFF9F0",
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
        self.cat_combo = ttk.Combobox(inner_container, 
                                      values=["食", "衣", "住", "行", "樂", "其他"], 
                                      width=8, 
                                      font=("Microsoft JhengHei", 11),
                                      state="readonly",
                                      takefocus=0)
        self.cat_combo.set("食")
        self.cat_combo.pack(side=tk.LEFT, padx=2)

        self.cat_combo.bind("<FocusIn>", lambda e: self.root.focus())
        self.cat_combo.bind("<<ComboboxSelected>>", lambda e: self.root.focus())

        # --- 花費 ---
        tk.Label(inner_container, text="花費", bg="#FDF5E6", fg=lbl_color, font=lbl_font).pack(side=tk.LEFT, padx=5)
        self.amount_entry = tk.Entry(inner_container, width=10, **entry_style)
        self.amount_entry.pack(side=tk.LEFT, padx=2)

        # --- 日期區塊 (年、月、日分別輸入) ---
        tk.Label(inner_container, text="日期", bg="#FDF5E6", fg=lbl_color, font=lbl_font).pack(side=tk.LEFT, padx=5)

        # 建立一個小容器來放置三個輸入框
        date_frame = tk.Frame(inner_container, bg="#FDF5E6")
        date_frame.pack(side=tk.LEFT, padx=5)

        # 年份 (4位數)
        self.year_entry = tk.Entry(date_frame, width=5, **entry_style)
        self.year_entry.insert(0, "2025")
        self.year_entry.pack(side=tk.LEFT)

        tk.Label(date_frame, text=" - ", bg="#FDF5E6").pack(side=tk.LEFT)

        # 月份 (2位數)
        self.month_entry = tk.Entry(date_frame, width=3, **entry_style)
        self.month_entry.insert(0, "12")
        self.month_entry.pack(side=tk.LEFT)

        tk.Label(date_frame, text=" - ", bg="#FDF5E6").pack(side=tk.LEFT)

        # 日 (2位數)
        self.day_entry = tk.Entry(date_frame, width=3, **entry_style)
        self.day_entry.insert(0, "19")
        self.day_entry.pack(side=tk.LEFT)

        # --- 新增按鈕 ---
        self.add_btn = tk.Button(inner_container, text="儲存", 
                                 command=self.handle_submit,
                                 bg="#A0522D", fg="white",
                                 font=("Microsoft JhengHei", 11, "bold"),
                                 relief="flat", padx=20, pady=3,
                                 activebackground="#8B4513", activeforeground="white",
                                 cursor="hand2")
        self.add_btn.pack(side=tk.LEFT, padx=20)

        self.delete_btn = tk.Button(inner_container, text="刪除選定 ", 
                                    command=self.handle_delete,
                                    bg="#CD5C5C", fg="white",
                                    font=("Microsoft JhengHei", 11, "bold"),
                                    relief="flat", padx=10, pady=3,
                                    cursor="hand2")
        self.delete_btn.pack(side=tk.LEFT, padx=10)

    def handle_submit(self):
        """收集數據並以字典格式存入 data_storage"""
        # 取得資料
        date = f"{self.year_entry.get()}-{self.month_entry.get()}-{self.day_entry.get()}"
        name = self.name_entry.get().strip()
        category = self.cat_combo.get().strip()
        amount = self.amount_entry.get().strip()
        

        # 驗證
        if not (name and category and amount and date):
            messagebox.showwarning("提示", "所有欄位都要填寫喔")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("錯誤", "花費請輸入數字喔")
            return
        
        # 執行儲存
        try:
            data_storage.save_expense(date,name, category, amount)
            messagebox.showinfo("成功", "資料已成功儲存！")
            self.name_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.refresh_ui()
            
        except Exception as e:
            messagebox.showerror("儲存失敗", f"發生錯誤：{e}")    

    def handle_delete(self):
        # 取得目前 Treeview 選取的項目
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("提示", "請先在上方清單點選要刪除的項目喔")
            return
        
        # 確認刪除
        if not messagebox.askyesno("確認刪除", "確定要刪除這筆帳目嗎？"):
            return

        item_index = self.tree.index(selected_item[0])

        try:
            if data_storage.delete_expense(item_index):
                messagebox.showinfo("成功", "資料已刪除")
                self.refresh_ui()
            else:
                messagebox.showerror("失敗", "找不到該筆資料")
        except Exception as e:
            messagebox.showerror("錯誤", f"刪除時發生錯誤：{e}")

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
    # --- 下拉選單主題 ---
    # 設定下拉選單的背景色
    root.option_add('*TCombobox*Listbox.background', '#FDF5E6') 
    # 設定下拉選單的文字顏色
    root.option_add('*TCombobox*Listbox.foreground', '#4B3621')
    # 設定選取時的背景色 (例如你的按鈕褐色)
    root.option_add('*TCombobox*Listbox.selectBackground', '#A0522D')
    # 設定選取時的文字顏色
    root.option_add('*TCombobox*Listbox.selectForeground', 'white')
    # 設定下拉選單的字體
    root.option_add('*TCombobox*Listbox.font', ("Microsoft JhengHei", 11))

    app = ExpenseApp(root)
    root.mainloop()