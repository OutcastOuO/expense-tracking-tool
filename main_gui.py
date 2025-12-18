import tkinter as tk
from tkinter import ttk

# --- 記帳工具gui ---
class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("記帳工具")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()