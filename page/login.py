import tkinter as tk
from tkinter import messagebox, ttk
from common.button import CustomButton
from query.quanLyTK import QuanLyTK

class LoginPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        # Kết nối tới cơ sở dữ liệu tài khoản (đọc file tk.csv)
        self.quanlytk = QuanLyTK("database/tk.csv", ["taikhoan", "matkhau", "sdt", "chucvu", "cccd"])
        self.view()

    def view(self):
        # Tiêu đề giao diện
        tk.Label(self.master, text="ĐĂNG NHẬP HỆ THỐNG", font=("Arial", 18, "bold"), fg="#e53935").pack(pady=25)

        # Khung chứa form nhập liệu
        form_frame = tk.Frame(self.master)
        form_frame.pack(pady=10, padx=40, fill="x")

        tk.Label(form_frame, text="Tài khoản:", font=("Arial", 11, "bold")).pack(anchor="w")
        self.ent_user = tk.Entry(form_frame, font=("Arial", 12))
        self.ent_user.pack(fill="x", pady=5)

        tk.Label(form_frame, text="Mật khẩu:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 0))
        self.ent_pass = tk.Entry(form_frame, font=("Arial", 12), show="*")
        self.ent_pass.pack(fill="x", pady=5)

        # --- DÒNG LIÊN KẾT QUÊN MẬT KHẨU (MỚI) ---
        lbl_forgot = tk.Label(form_frame, text="Quên mật khẩu?", font=("Arial", 10, "underline", "italic"), fg="#1976D2", cursor="hand2")
        lbl_forgot.pack(anchor="e", pady=5)
        lbl_forgot.bind("<Button-1>", self.open_forgot_password_window) # Click chuột trái để mở cửa sổ lấy lại MK

        # --- KHU VỰC CÁC NÚT BẤM (CẬP NHẬT) ---
        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=20)

        # Nút Đăng nhập chính
        CustomButton(btn_frame, text="ĐĂNG NHẬP", command=self.login, style_type="danger", width=15).pack(side="left", padx=10)
        
        # Nút Thoát chương trình (MỚI)
        CustomButton(btn_frame, text="THOÁT APP", command=self.exit_application, style_type="secondary", width=15).pack(side="left", padx=10)

    def login(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()

        if not u or not p:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ tài khoản và mật khẩu!")
            return

        if self.quanlytk.checkLogin(u, p):
            # --- Tạm thời comment logic đọc phân quyền để giữ luồng cơ bản ---
            self.app_manager.current_user = u
            self.app_manager.current_role = "quản lý" # Mặc định quyền cao nhất để test cho mượt
            
            messagebox.showinfo("Thành công", f"Chào mừng {u} đã quay trở lại!")
            self.app_manager.show_home_page()
        else:
            messagebox.showerror("Thất bại", "Tài khoản hoặc mật khẩu không chính xác!")

    def exit_application(self):
        """Hàm đóng toàn bộ ứng dụng an toàn (MỚI)"""
        if messagebox.askyesno("Xác nhận thoát", "Bạn có chắc chắn muốn đóng hệ thống WinMart?"):
            self.master.destroy()

    def open_forgot_password_window(self, event=None):
        """Hàm mở cửa sổ phụ phục vụ lấy lại mật khẩu qua CCCD (MỚI)"""
        # Tạo một cửa sổ con nằm đè lên trên
        forgot_win = tk.Toplevel(self.master)
        forgot_win.title("Lấy lại mật khẩu")
        forgot_win.geometry("350x250")
        forgot_win.resizable(False, False)
        forgot_win.grab_set() # Ngăn tương tác với cửa sổ chính khi chưa tắt cửa sổ này

        tk.Label(forgot_win, text="KHÔI PHỤC MẬT KHẨU", font=("Arial", 13, "bold"), fg="#1976D2").pack(pady=15)

        # Form nhập thông tin xác minh
        sub_frame = tk.Frame(forgot_win)
        sub_frame.pack(padx=20, fill="x")

        tk.Label(sub_frame, text="Nhập tên tài khoản:").pack(anchor="w")
        ent_forgot_user = tk.Entry(sub_frame, font=("Arial", 11))
        ent_forgot_user.pack(fill="x", pady=5)

        tk.Label(sub_frame, text="Nhập số CCCD xác minh:").pack(anchor="w", pady=(5, 0))
        ent_forgot_cccd = tk.Entry(sub_frame, font=("Arial", 11))
        ent_forgot_cccd.pack(fill="x", pady=5)

        def verify_and_get_password():
            u_check = ent_forgot_user.get().strip()
            c_check = ent_forgot_cccd.get().strip()

            if not u_check or not c_check:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ thông tin xác minh!", parent=forgot_win)
                return

            try:
                # Đọc file csv tài khoản bằng pandas để tìm thông tin
                import pandas as pd
                df = pd.read_csv("database/tk.csv")
                
                # Tìm dòng khớp cả tài khoản lẫn số CCCD
                match = df[(df['taikhoan'].astype(str) == str(u_check)) & (df['cccd'].astype(str) == str(c_check))]
                
                if not match.empty:
                    # Lấy ra mật khẩu ở dòng đó
                    password_retrieved = match.iloc[0]['matkhau']
                    messagebox.showinfo("Thành công", f"Xác minh đúng!\nMật khẩu của tài khoản '{u_check}' là: {password_retrieved}", parent=forgot_win)
                    forgot_win.destroy() # Đóng cửa sổ khôi phục lại
                else:
                    messagebox.showerror("Lỗi xác minh", "Tài khoản hoặc số CCCD không khớp trong hệ thống!", parent=forgot_win)
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Không thể đọc cơ sở dữ liệu: {e}", parent=forgot_win)

        # Nút thực hiện xác minh
        CustomButton(forgot_win, text="XÁC MINH CẤP LẠI", command=verify_and_get_password, style_type="primary").pack(pady=15)