import tkinter as tk
from tkinter import ttk
import pandas as pd
from common.button import CustomButton

class HomePage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.view()

    def get_stats(self):
        """Lấy số liệu thực tế từ CSV để hiển thị lên các thẻ"""
        try:
            # Đọc file sản phẩm
            df_sp = pd.read_csv("database/sanpham.csv")
            total_sp = len(df_sp)
            # Cảnh báo nếu số lượng sản phẩm trong kho < 5
            low_stock = len(df_sp[df_sp['so_luong'] < 5])
            
            # Đọc file tài khoản nhân viên
            df_tk = pd.read_csv("database/tk.csv")
            total_nv = len(df_tk)
        except Exception as e:
            print(f"Lỗi đọc dữ liệu: {e}")
            total_sp = total_nv = low_stock = 0
        return total_sp, total_nv, low_stock

    def view(self):
        # Tiêu đề trang chủ
        tk.Label(self.master, text="BẢNG ĐIỀU KHIỂN WINMART", 
                 font=("Arial", 25, "bold"), fg="#e53935").pack(pady=30)
        
        # Lấy dữ liệu thống kê
        total_sp, total_nv, low_stock = self.get_stats()

        # --- Khu vực các thẻ Thống kê (Cards) ---
        card_frame = tk.Frame(self.master)
        card_frame.pack(pady=20)

        self.create_card(card_frame, "TỔNG SẢN PHẨM", total_sp, "#4CAF50").grid(row=0, column=0, padx=20)
        self.create_card(card_frame, "NHÂN VIÊN", total_nv, "#2196F3").grid(row=0, column=1, padx=20)
        self.create_card(card_frame, "SẮP HẾT HÀNG", low_stock, "#F44336").grid(row=0, column=2, padx=20)

        # --- Khu vực các nút bấm điều hướng (Menu chính) ---
        menu_frame = tk.LabelFrame(self.master, text="Chức năng hệ thống", font=("Arial", 12, "italic"))
        menu_frame.pack(pady=30, padx=50, fill="x")

        btn_container = tk.Frame(menu_frame)
        btn_container.pack(pady=20)

        # 1. Nút đi tới trang Thanh toán (Bán hàng)
        CustomButton(btn_container, text="BÁN HÀNG (THANH TOÁN)", 
                     command=self.app_manager.show_checkout_page, 
                     style_type="success", width=25).grid(row=0, column=0, padx=15, pady=10)

        # 2. Nút đi tới trang Quản lý Kho
        CustomButton(btn_container, text="QUẢN LÝ KHO HÀNG", 
                     command=self.app_manager.show_inventory_page, 
                     style_type="info", width=25).grid(row=0, column=1, padx=15, pady=10)

        # 3. Nút đi tới trang Quản lý Nhân viên
        CustomButton(btn_container, text="QUẢN LÝ NHÂN VIÊN", 
                     command=self.app_manager.show_manage_staff_page, 
                     style_type="primary", width=25).grid(row=1, column=0, padx=15, pady=10)

        # 4. Nút Đăng xuất quay về màn hình Login
        CustomButton(btn_container, text="ĐĂNG XUẤT", 
                     command=self.app_manager.show_login_page, 
                     style_type="secondary", width=25).grid(row=1, column=1, padx=15, pady=10)

    def create_card(self, parent, title, value, color):
        """Hàm vẽ các ô thống kê"""
        card = tk.Frame(parent, bg=color, width=220, height=130, bd=0, relief="flat")
        card.pack_propagate(False)
        tk.Label(card, text=title, bg=color, fg="white", font=("Arial", 11, "bold")).pack(pady=(15, 5))
        tk.Label(card, text=str(value), bg=color, fg="white", font=("Arial", 30, "bold")).pack()
        return card