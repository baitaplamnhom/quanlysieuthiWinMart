import tkinter as tk
from tkinter import ttk
import pandas as pd
from common.button import CustomButton


class HomePage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        self.master.configure(bg="#f4f6f9")

        self.view()

    # ===================== ĐỌC DỮ LIỆU =====================
    def get_stats(self):
        try:
            df_sp = pd.read_csv("database/sanpham.csv")
            total_sp = len(df_sp)

            low_stock = len(df_sp[df_sp['so_luong'] < 5])

            df_tk = pd.read_csv("database/tk.csv")
            total_nv = len(df_tk)

        except Exception as e:
            print("Lỗi đọc dữ liệu:", e)
            total_sp = total_nv = low_stock = 0

        return total_sp, total_nv, low_stock

    # ===================== GIAO DIỆN =====================
    def view(self):

        # ===================== HEADER =====================
        header = tk.Frame(self.master, bg="#d70018", height=120)
        header.pack(fill="x")

        header.pack_propagate(False)

        title_frame = tk.Frame(header, bg="#d70018")
        title_frame.pack(pady=25)

        tk.Label(
            title_frame,
            text="🛒 HỆ THỐNG QUẢN LÝ WINMART",
            bg="#d70018",
            fg="white",
            font=("Arial", 26, "bold")
        ).pack()

        # ===================== MAIN =====================
        main_frame = tk.Frame(self.master, bg="#f4f6f9")
        main_frame.pack(fill="both", expand=True, padx=30, pady=25)

        total_sp, total_nv, low_stock = self.get_stats()

        tk.Label(
            main_frame,
            text="📊 TỔNG QUAN HỆ THỐNG",
            bg="#f4f6f9",
            fg="#222",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", pady=(0, 20))

        card_frame = tk.Frame(main_frame, bg="#f4f6f9")
        card_frame.pack()

        self.create_card(
            card_frame,
            "📦 TỔNG SẢN PHẨM",
            total_sp,
            "#4CAF50"
        ).grid(row=0, column=0, padx=20)

        self.create_card(
            card_frame,
            "👨‍💼 NHÂN VIÊN",
            total_nv,
            "#2196F3"
        ).grid(row=0, column=1, padx=20)

        self.create_card(
            card_frame,
            "⚠️ SẮP HẾT HÀNG",
            low_stock,
            "#F44336"
        ).grid(row=0, column=2, padx=20)

        # ===================== MENU =====================
        menu_frame = tk.Frame(
            main_frame,
            bg="white",
            bd=0,
            relief="flat"
        )
        menu_frame.pack(fill="x", pady=40)

        tk.Label(
            menu_frame,
            text="⚙️ CHỨC NĂNG HỆ THỐNG",
            bg="white",
            fg="#333",
            font=("Arial", 18, "bold")
        ).pack(pady=(20, 25))

        btn_frame = tk.Frame(menu_frame, bg="white")
        btn_frame.pack(pady=10)

        # ===== BUTTONS =====
        CustomButton(
            btn_frame,
            text="🛒 BÁN HÀNG",
            command=self.app_manager.show_checkout_page,
            style_type="success",
            width=28
        ).grid(row=0, column=0, padx=20, pady=15)

        CustomButton(
            btn_frame,
            text="📦 QUẢN LÝ KHO",
            command=self.app_manager.show_inventory_page,
            style_type="info",
            width=28
        ).grid(row=0, column=1, padx=20, pady=15)

        CustomButton(
            btn_frame,
            text="👨‍💼 QUẢN LÝ NHÂN VIÊN",
            command=self.app_manager.show_manage_staff_page,
            style_type="primary",
            width=28
        ).grid(row=1, column=0, padx=20, pady=15)

        CustomButton(
            btn_frame,
            text="🚪 ĐĂNG XUẤT",
            command=self.app_manager.show_login_page,
            style_type="secondary",
            width=28
        ).grid(row=1, column=1, padx=20, pady=15)

        # ===================== FOOTER =====================
        footer = tk.Frame(self.master, bg="#d70018", height=40)
        footer.pack(fill="x", side="bottom")

        tk.Button(
            footer,
            text="ℹ Giới thiệu phần mềm",
            bg="#d70018",
            fg="white",
            activebackground="#b30014",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            font=("Arial", 10, "bold"),
            command=self.show_about
        ).pack(pady=8)

    # ===================== CARD =====================
    def create_card(self, parent, title, value, color):

        card = tk.Frame(
            parent,
            bg=color,
            width=250,
            height=150,
            bd=0,
            relief="flat",
            cursor="hand2"
        )

        card.grid_propagate(False)

        def on_enter(e):
            card.config(bg=self.lighten_color(color))

        def on_leave(e):
            card.config(bg=color)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        tk.Label(
            card,
            text=title,
            bg=color,
            fg="white",
            font=("Arial", 13, "bold")
        ).pack(pady=(22, 10))

        tk.Label(
            card,
            text=str(value),
            bg=color,
            fg="white",
            font=("Arial", 38, "bold")
        ).pack()

        return card

    # ===================== ABOUT =====================
    def show_about(self):
        about = tk.Toplevel(self.master)
        about.title("About")
        about.geometry("560x320")
        about.resizable(False, False)
        about.configure(bg="#f2f2f2")

        tk.Label(
            about,
            text="PHẦN MỀM QUẢN LÝ WINMART",
            font=("Arial", 18, "bold"),
            bg="#f2f2f2"
        ).pack(pady=20)

        info = """
Phiên bản: 1.5
Tác giả: Trần Hoàng - Văn Dũng - Quang Anh - Xuân Trường
Đơn vị: Khoa CNTT - Trường Đại Học Hạ Long
Ngày phát hành: 01/06/2026
"""

        tk.Label(
            about,
            text=info,
            justify="left",
            bg="#f2f2f2",
            font=("Arial", 12)
        ).pack(pady=10)

        tk.Button(
            about,
            text="Đóng",
            width=15,
            bg="#4A90E2",
            fg="white",
            font=("Arial", 11, "bold"),
            command=about.destroy
        ).pack(pady=20)

        about.transient(self.master)
        about.grab_set()

    # ===================== LÀM SÁNG MÀU =====================
    def lighten_color(self, color):
        colors = {
            "#4CAF50": "#66BB6A",
            "#2196F3": "#42A5F5",
            "#F44336": "#EF5350"
        }
        return colors.get(color, color)