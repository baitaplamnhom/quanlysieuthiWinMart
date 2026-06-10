import tkinter as tk
from tkinter import messagebox, ttk
from common.button import CustomButton
from query.quanLyTK import QuanLyTK


class QuanLyTKPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        # Màu nền chính
        self.master.configure(bg="#f4f6f9")

        # Kết nối dữ liệu tài khoản
        self.quanlytk = QuanLyTK(
            "database/tk.csv",
            ["taikhoan", "matkhau", "sdt", "chucvu", "cccd"]
        )

        self.view()
        self.load_accounts()

    def view(self):

        # ================= HEADER =================
        header = tk.Frame(self.master, bg="#d70018", height=85)
        header.pack(fill="x")

        header.pack_propagate(False)

        tk.Label(
            header,
            text="👨‍💼 QUẢN LÝ NHÂN VIÊN WINMART",
            bg="#d70018",
            fg="white",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # ================= MAIN =================
        main_frame = tk.Frame(self.master, bg="#f4f6f9")
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # ================= FRAME NHẬP LIỆU =================
        ifrm = tk.LabelFrame(
            main_frame,
            text=" Thông tin nhân viên ",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333",
            bd=2,
            relief="groove"
        )

        ifrm.pack(fill="x", pady=10)

        # ===== STYLE =====
        label_style = {
            "font": ("Arial", 11, "bold"),
            "bg": "white",
            "fg": "#333"
        }

        entry_style = {
            "font": ("Arial", 11),
            "bd": 2,
            "relief": "groove"
        }

        # ===== DÒNG 1 =====
        tk.Label(ifrm, text="Tài khoản:", **label_style).grid(
            row=0, column=0, padx=10, pady=12, sticky="e"
        )

        self.ent_user = tk.Entry(
            ifrm,
            width=25,
            **entry_style
        )

        self.ent_user.grid(
            row=0,
            column=1,
            padx=10,
            pady=12
        )

        tk.Label(ifrm, text="Mật khẩu:", **label_style).grid(
            row=0,
            column=2,
            padx=10,
            pady=12,
            sticky="e"
        )

        self.ent_pass = tk.Entry(
            ifrm,
            show="*",
            width=25,
            **entry_style
        )

        self.ent_pass.grid(
            row=0,
            column=3,
            padx=10,
            pady=12
        )

        # ===== DÒNG 2 =====
        tk.Label(ifrm, text="SĐT:", **label_style).grid(
            row=1,
            column=0,
            padx=10,
            pady=12,
            sticky="e"
        )

        self.ent_sdt = tk.Entry(
            ifrm,
            width=25,
            **entry_style
        )

        self.ent_sdt.grid(
            row=1,
            column=1,
            padx=10,
            pady=12
        )

        tk.Label(ifrm, text="Chức vụ:", **label_style).grid(
            row=1,
            column=2,
            padx=10,
            pady=12,
            sticky="e"
        )

        self.cb_chucvu = ttk.Combobox(
            ifrm,
            values=["quản lý", "nhân viên"],
            state="readonly",
            font=("Arial", 10),
            width=22
        )

        self.cb_chucvu.grid(
            row=1,
            column=3,
            padx=10,
            pady=12
        )

        self.cb_chucvu.current(1)

        # ===== DÒNG 3 =====
        tk.Label(ifrm, text="Số CCCD:", **label_style).grid(
            row=2,
            column=0,
            padx=10,
            pady=12,
            sticky="e"
        )

        self.ent_cccd = tk.Entry(
            ifrm,
            width=25,
            **entry_style
        )

        self.ent_cccd.grid(
            row=2,
            column=1,
            padx=10,
            pady=12
        )

        # ================= NÚT CHỨC NĂNG =================
        bfrm = tk.Frame(main_frame, bg="#f4f6f9")
        bfrm.pack(pady=15)

        CustomButton(
            bfrm,
            text="➕ Thêm nhân viên",
            command=self.add_account,
            style_type="success",
            width=22
        ).pack(side="left", padx=10)

        CustomButton(
            bfrm,
            text="🗑️ Xóa nhân viên",
            command=self.delete_account,
            style_type="danger",
            width=22
        ).pack(side="left", padx=10)

        # ===== QUAY LẠI TRANG CHỦ =====
        CustomButton(
            bfrm,
            text="⬅ Quay lại Trang chủ",
            command=self.app_manager.show_home_page,
            style_type="secondary",
            width=24
        ).pack(side="left", padx=10)

        # ================= STYLE TREEVIEW =================
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=35,
            fieldbackground="white",
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#d70018",
            foreground="white",
            font=("Arial", 11, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#4CAF50")],
            foreground=[("selected", "white")]
        )

        # ================= BẢNG DỮ LIỆU =================
        table_frame = tk.Frame(main_frame, bg="white")
        table_frame.pack(fill="both", expand=True, pady=10)

        cols = (
            "Tài khoản",
            "Mật khẩu",
            "SĐT",
            "Chức vụ",
            "CCCD"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=cols,
            show="headings",
            height=10
        )

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=180, anchor="center")

        # ===== SCROLLBAR =====
        scroll_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scroll_y.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_y.pack(side="right", fill="y")

        # ================= FOOTER =================
        footer = tk.Frame(self.master, bg="#d70018", height=35)
        footer.pack(fill="x", side="bottom")

        tk.Label(
            footer,
            text="WinMart Employee Management © 2026",
            bg="#d70018",
            fg="white",
            font=("Arial", 9)
        ).pack(pady=7)

    # ================= LOAD DỮ LIỆU =================
    def load_accounts(self):

        for i in self.tree.get_children():
            self.tree.delete(i)

        res = self.quanlytk.list(1, 100)
        data = res["data"]

        for item in data.values:
            self.tree.insert("", "end", values=list(item))

    # ================= THÊM TÀI KHOẢN =================
    def add_account(self):

        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        s = self.ent_sdt.get().strip()
        cv = self.cb_chucvu.get()
        c = self.ent_cccd.get().strip()

        if not all([u, p, s, cv, c]):

            messagebox.showwarning(
                "Lỗi",
                "Vui lòng nhập đầy đủ thông tin!"
            )

            return

        data = [u, p, s, cv, c]

        if self.quanlytk.create(data):

            messagebox.showinfo(
                "Thành công",
                f"Đã thêm tài khoản: {u}"
            )

            self.load_accounts()
            self.clear_fields()

    # ================= XÓA TÀI KHOẢN =================
    def delete_account(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Lỗi",
                "Hãy chọn nhân viên cần xóa!"
            )

            return

        acc_name = self.tree.item(selected[0])['values'][0]

        if messagebox.askyesno(
            "Xác nhận",
            f"Bạn có chắc muốn xóa nhân viên {acc_name}?"
        ):

            if self.quanlytk.delete(
                "taikhoan",
                str(acc_name)
            ):

                messagebox.showinfo(
                    "Thành công",
                    "Đã xóa nhân viên!"
                )

                self.load_accounts()

    # ================= CLEAR INPUT =================
    def clear_fields(self):

        self.ent_user.delete(0, 'end')
        self.ent_pass.delete(0, 'end')
        self.ent_sdt.delete(0, 'end')
        self.ent_cccd.delete(0, 'end')