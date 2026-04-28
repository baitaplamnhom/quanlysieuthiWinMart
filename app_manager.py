import tkinter as tk
from page.login import LoginPage
from page.quanlysp import QuanLySPPage
from page.quanlytk import QuanLyTKPage
from page.home import HomePage
from page.thanhtoan import ThanhToanPage

class AppManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hệ thống Quản lý WinMart")
        self.current_page = None
        
        # Luôn bắt đầu ứng dụng tại trang Đăng nhập
        self.show_login_page()

    def run(self):
        """Chạy vòng lặp chính của ứng dụng"""
        self.root.mainloop()

    def clear_current_page(self):
        """Xóa toàn bộ các widget của trang cũ trước khi chuyển trang mới"""
        if self.current_page:
            for widget in self.root.winfo_children():
                widget.destroy()

    def show_login_page(self):
        """Hiển thị trang Đăng nhập"""
        self.clear_current_page()
        self.root.geometry("400x450")
        self.current_page = LoginPage(self.root, self)

    def show_home_page(self):
        """Hiển thị trang Chủ (Dashboard)"""
        self.clear_current_page()
        self.root.geometry("1000x700")
        self.current_page = HomePage(self.root, self)

    def show_inventory_page(self):
        """Hiển thị trang Quản lý Kho (Sản phẩm)"""
        self.clear_current_page()
        self.root.geometry("1100x700")
        self.current_page = QuanLySPPage(self.root, self)

    def show_manage_staff_page(self):
        """Hiển thị trang Quản lý Nhân viên (Tài khoản)"""
        self.clear_current_page()
        self.root.geometry("1100x700")
        self.current_page = QuanLyTKPage(self.root, self)

    def show_checkout_page(self):
        """Hiển thị trang Thanh toán (Bán hàng)"""
        self.clear_current_page()
        self.root.geometry("1100x750")
        self.current_page = ThanhToanPage(self.root, self)