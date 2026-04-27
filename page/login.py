import tkinter as tk
from tkinter import messagebox
from common.button import CustomButton
from query.quanLyTK import QuanLyTK

class LoginPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        # Cấu hình cửa sổ
        self.master.title("WinMart Login")
        self.master.geometry("400x450")
        self.master.configure(bg="#f0f2f5")

        self.quanlytk = QuanLyTK("database/tk.csv",["taikhoan","matkhau","sdt","chucvu","cccd"])

        self.view()
    def view(self):
        # ======= Frame chính =======
        main_frame = tk.Frame(self.master, bg="white", bd=2, relief="groove")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=360)

        # ======= Tiêu đề =======
        tk.Label(main_frame, text="WINMART", 
                 font=("Arial", 20, "bold"), 
                 fg="#e53935", bg="white").pack(pady=(20,5))

        tk.Label(main_frame, text="Đăng nhập hệ thống", 
                 font=("Arial", 11), 
                 bg="white").pack(pady=(0,15))

        # ======= Username =======
        tk.Label(main_frame, text="Username", 
                 bg="white", anchor="w").pack(fill="x", padx=20)
        
        self.ent_user = tk.Entry(main_frame, bd=1, relief="solid")
        self.ent_user.pack(padx=20, pady=5, fill="x")

        # ======= Password =======
        tk.Label(main_frame, text="Password", 
                 bg="white", anchor="w").pack(fill="x", padx=20)
        
        self.ent_pass = tk.Entry(main_frame, show="*", bd=1, relief="solid")
        self.ent_pass.pack(padx=20, pady=5, fill="x")

        # ======= Nút đăng nhập =======
        btn_login = tk.Button(main_frame, text="Đăng nhập",
                              bg="#4CAF50", fg="white",
                              font=("Arial", 10, "bold"),
                              bd=0, height=2,
                              command=self.login)
        btn_login.pack(padx=20, pady=(20,10), fill="x")

        # ======= Nút thoát =======
        btn_exit = tk.Button(main_frame, text="Thoát",
                             bg="#f44336", fg="white",
                             font=("Arial", 10, "bold"),
                             bd=0, height=2,
                             command=self.master.quit)
        btn_exit.pack(padx=20, fill="x")

        # ======= Footer nhỏ =======
        tk.Label(main_frame, text="© WinMart System", 
                 bg="white", fg="gray", font=("Arial", 8)).pack(side="bottom", pady=10)
    def login(self):
        # Test nhanh với admin/123456
        if self.quanlytk.checkLogin(self.ent_user.get(),self.ent_pass.get()) :
            self.app_manager.show_inventory_page()
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")