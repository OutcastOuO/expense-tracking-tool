import tkinter as tk
from tkinter import ttk, messagebox

import data_storage

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("記帳工具")
        self.root.geometry("1400x720")
        self.root.configure(background="#FDF5E6")

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
        
        # input bar
        self.setup_input_bar()

    def setup_input_bar(self):
        # 欄容器
        self.bottom_bar = tk.Frame(self.root, pady=0, bg="#FDF5E6")
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
        self.add_btn = tk.Button(inner_container, text="  儲存 ", 
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

    def refresh_ui(self):
        pass

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