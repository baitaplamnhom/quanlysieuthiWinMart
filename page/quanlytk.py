import tkinter as tk
from tkinter import messagebox, ttk
from common.button import CustomButton
from query.quanLyTK import QuanLyTK

class QuanLyTKPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        # Kết nối dữ liệu tài khoản (5 cột: taikhoan, matkhau, sdt, chucvu, cccd)
        self.quanlytk = QuanLyTK("database/tk.csv", ["taikhoan", "matkhau", "sdt", "chucvu", "cccd"])
        self.view()
        self.load_accounts()

    def view(self):
        # --- Tiêu đề ---
        tk.Label(self.master, text="QUẢN LÝ NHÂN VIÊN WINMART", 
                 font=("Arial", 20, "bold"), fg="#e53935").pack(pady=10)

        # --- Frame Nhập liệu ---
        ifrm = tk.LabelFrame(self.master, text="Thông tin nhân viên")
        ifrm.pack(fill="x", padx=20, pady=10)

        # Dòng 1: Tài khoản & Mật khẩu
        tk.Label(ifrm, text="Tài khoản:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_user = tk.Entry(ifrm, font=("Arial", 11))
        self.ent_user.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ifrm, text="Mật khẩu:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_pass = tk.Entry(ifrm, show="*", font=("Arial", 11))
        self.ent_pass.grid(row=0, column=3, padx=5, pady=5)

        # Dòng 2: SĐT & Chức vụ
        tk.Label(ifrm, text="SĐT:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_sdt = tk.Entry(ifrm, font=("Arial", 11))
        self.ent_sdt.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ifrm, text="Chức vụ:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.cb_chucvu = ttk.Combobox(ifrm, values=["quản lý", "nhân viên"], state="readonly")
        self.cb_chucvu.grid(row=1, column=3, padx=5, pady=5)
        self.cb_chucvu.current(1)

        # Dòng 3: Số CCCD
        tk.Label(ifrm, text="Số CCCD:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.ent_cccd = tk.Entry(ifrm, font=("Arial", 11))
        self.ent_cccd.grid(row=2, column=1, padx=5, pady=5)

        # --- Frame Nút chức năng (Thêm/Xóa) ---
        bfrm = tk.Frame(self.master)
        bfrm.pack(pady=10)

        CustomButton(bfrm, text="Thêm nhân viên", command=self.add_account, style_type="success").pack(side="left", padx=5)
        CustomButton(bfrm, text="Xóa nhân viên", command=self.delete_account, style_type="danger").pack(side="left", padx=5)

        # --- Bảng hiển thị (Treeview) ---
        cols = ("Tài khoản", "Mật khẩu", "SĐT", "Chức vụ", "CCCD")
        self.tree = ttk.Treeview(self.master, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # --- NÚT QUAY LẠI TRANG CHỦ (Đặt dưới cùng để đồng bộ hệ thống) ---
        CustomButton(self.master, text="Quay lại Trang chủ", 
                     command=self.app_manager.show_home_page, 
                     style_type="secondary").pack(pady=20)

    def load_accounts(self):
        """Nạp danh sách nhân viên từ file CSV lên bảng"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        res = self.quanlytk.list(1, 100)
        data = res["data"]
        # Duyệt qua dữ liệu (DataFrame của Pandas)
        for item in data.values:
            self.tree.insert("", "end", values=list(item))

    def add_account(self):
        """Xử lý thêm tài khoản mới"""
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        s = self.ent_sdt.get().strip()
        cv = self.cb_chucvu.get()
        c = self.ent_cccd.get().strip()

        if not all([u, p, s, cv, c]):
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        data = [u, p, s, cv, c]
        if self.quanlytk.create(data):
            messagebox.showinfo("Thành công", f"Đã thêm tài khoản: {u}")
            self.load_accounts()
            self.clear_fields()

    def delete_account(self):
        """Xóa tài khoản được chọn"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Lỗi", "Hãy chọn nhân viên cần xóa!")
            return

        acc_name = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa nhân viên {acc_name}?"):
            if self.quanlytk.delete("taikhoan", str(acc_name)):
                messagebox.showinfo("Thành công", "Đã xóa nhân viên!")
                self.load_accounts()

    def clear_fields(self):
        """Dọn sạch các ô nhập liệu"""
        self.ent_user.delete(0, 'end')
        self.ent_pass.delete(0, 'end')
        self.ent_sdt.delete(0, 'end')
        self.ent_cccd.delete(0, 'end')