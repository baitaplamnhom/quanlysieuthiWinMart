
import tkinter as tk
from page.login import LoginPage
from page.quanlysp import QuanLySPPage

class AppManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hệ thống Quản lý WinMart")
        self.current_page = None
        self.show_inventory_page()

    def run(self):
        self.root.mainloop()

    def clear_current_page(self):
        if self.current_page:
            for widget in self.root.winfo_children():
                widget.destroy()

    def show_login_page(self):
        self.clear_current_page()
        self.root.geometry("350x250")
        self.current_page = LoginPage(self.root, self)

    def show_inventory_page(self):
        self.clear_current_page()
        self.root.geometry("900x650")
        self.current_page = QuanLySPPage(self.root, self)