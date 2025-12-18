import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import chart_generator

# --- 記帳工具 GUI ---
class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("記帳工具")

        self.fig, self.axis = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 初始載入圖表
        self.refresh_ui()
    
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def refresh_ui(self):
        current_data = [
            {"amount": "350", "category": "食"},
            {"amount": "60", "category": "行"},
            {"amount": "500", "category": "衣"},
            {"amount": "1200", "category": "樂"},
            {"amount": "2000", "category": "住"}
        ]
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