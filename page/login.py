import tkinter as tk
from tkinter import messagebox
from common.button import CustomButton
from query.quanLyTK import QuanLyTK

class LoginPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.master.configure(bg="#f5f5f5")

        # Kết nối CSDL
        self.quanlytk = QuanLyTK("database/tk.csv", ["taikhoan", "matkhau", "sdt", "chucvu", "cccd"])
        self.view()

    def view(self):
        # ===== KHUNG CHÍNH (CENTER) =====
        main_frame = tk.Frame(self.master, bg="#f5f5f5")
        main_frame.pack(expand=True)

        # ===== CARD LOGIN =====
        card = tk.Frame(main_frame, bg="white", bd=2, relief="groove")
        card.pack(pady=50, padx=20)

        # ===== TIÊU ĐỀ =====
        tk.Label(card, text="ĐĂNG NHẬP", font=("Arial", 20, "bold"), 
                 fg="#e53935", bg="white").pack(pady=20)

        # ===== FORM =====
        form_frame = tk.Frame(card, bg="white")
        form_frame.pack(padx=30, pady=10)

        # USERNAME
        tk.Label(form_frame, text="Tài khoản", bg="white", anchor="w").pack(fill="x")
        self.ent_user = tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid")
        self.ent_user.pack(fill="x", pady=8, ipady=5)

        # PASSWORD
        tk.Label(form_frame, text="Mật khẩu", bg="white", anchor="w").pack(fill="x")
        self.ent_pass = tk.Entry(form_frame, font=("Arial", 12), show="*", bd=1, relief="solid")
        self.ent_pass.pack(fill="x", pady=8, ipady=5)

        # ===== NÚT LOGIN =====
        CustomButton(card, text="ĐĂNG NHẬP", command=self.login, 
                     style_type="danger", width=25).pack(pady=20)

        # ===== FOOTER =====
        tk.Label(card, text="© 2026 Hệ thống quản lý", 
                 font=("Arial", 9), fg="gray", bg="white").pack(pady=(0, 10))

    def login(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()

        if not u or not p:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ tài khoản và mật khẩu!")
            return

        if self.quanlytk.checkLogin(u, p):
            messagebox.showinfo("Thành công", f"Chào mừng {u} đã quay trở lại!")
            self.app_manager.show_home_page()
        else:
            messagebox.showerror("Thất bại", "Tài khoản hoặc mật khẩu không chính xác!")