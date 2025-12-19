import tkinter as tk
from tkinter import ttk, messagebox

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("暖心記帳工具")
        self.root.geometry("1200x720")
        self.root.configure(bg="#FDF5E6") # 視窗大背景

        # 設定整體 Style (讓 Combobox 也能套用主題)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # 呼叫 UI 組件
        self.setup_input_bar()

    def setup_input_bar(self):
        """美化後的輸入底欄 - 手動輸入日期版本"""
        
        # 1. 建立底欄容器 (顏色與背景融合)
        self.bottom_bar = tk.Frame(self.root, pady=25, bg="#FDF5E6")
        self.bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 頂部裝飾線 (營造質感)
        separator = tk.Frame(self.bottom_bar, height=1, bg="#D2B48C")
        separator.pack(fill=tk.X, side=tk.TOP, pady=(0, 20))

        # 內部水平容器 (讓所有元件靠中排列)
        inner_container = tk.Frame(self.bottom_bar, bg="#FDF5E6")
        inner_container.pack(expand=True)

        # 設定風格參數
        lbl_style = {"bg": "#FDF5E6", "fg": "#4B3621", "font": ("Microsoft JhengHei", 11, "bold")}
        # Entry 的統一樣式：平坦、帶有一像素的褐色邊框
        entry_opts = {
            "font": ("Microsoft JhengHei", 11),
            "relief": "flat",
            "highlightthickness": 1,
            "highlightbackground": "#D2B48C",
            "highlightcolor": "#8B4513" # 點擊時顏色加深
        }

        # --- 1. 名稱 ---
        tk.Label(inner_container, text="品名:", **lbl_style).pack(side=tk.LEFT, padx=(10, 5))
        self.name_entry = tk.Entry(inner_container, width=15, **entry_opts)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        # --- 2. 類別 ---
        tk.Label(inner_container, text="類別:", **lbl_style).pack(side=tk.LEFT, padx=(10, 5))
        self.cat_combo = ttk.Combobox(inner_container, values=["食", "衣", "住", "行", "樂"], width=8, font=("Microsoft JhengHei", 11))
        self.cat_combo.pack(side=tk.LEFT, padx=5)

        # --- 3. 花費 ---
        tk.Label(inner_container, text="花費:", **lbl_style).pack(side=tk.LEFT, padx=(10, 5))
        self.amount_entry = tk.Entry(inner_container, width=10, **entry_opts)
        self.amount_entry.pack(side=tk.LEFT, padx=5)

        # --- 4. 日期 (使用者自行設定) ---
        tk.Label(inner_container, text="日期:", **lbl_style).pack(side=tk.LEFT, padx=(10, 5))
        self.date_entry = tk.Entry(inner_container, width=12, **entry_opts)
        self.date_entry.insert(0, "2025-12-19") # 保持原有的手動提示格式
        self.date_entry.pack(side=tk.LEFT, padx=5)

        # --- 5. 新增按鈕 ---
        self.add_btn = tk.Button(inner_container, text=" ＋ 記帳 ", 
                                 command=self.handle_submit,
                                 bg="#A0522D", fg="white",
                                 font=("Microsoft JhengHei", 11, "bold"),
                                 relief="flat", padx=20, pady=3,
                                 activebackground="#8B4513", activeforeground="white",
                                 cursor="hand2")
        self.add_btn.pack(side=tk.LEFT, padx=25)

    def handle_submit(self):
        # 取得資料並去除首尾空格
        amount = self.amount_entry.get().strip()
        category = self.cat_combo.get().strip()
        name = self.name_entry.get().strip()
        date = self.date_entry.get().strip()

        # 驗證
        if not (name and category and amount and date):
            messagebox.showwarning("提示", "溫馨提醒：所有欄位都要填寫喔 😊")
            return

        try:
            amount_val = float(amount)
        except ValueError:
            messagebox.showerror("錯誤", "金額請輸入數字喔！")
            return

        # 這裡連接你的資料處理邏輯...
        print(f"準備儲存：{date} {name} {category} ${amount_val}")
        
        # 成功後清理 (不清理日期與類別，方便快速輸入下一筆)
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()