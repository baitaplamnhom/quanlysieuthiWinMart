import tkinter as tk
from tkinter import messagebox, ttk
import time
import pandas as pd
from common.button import CustomButton
from query.quanLySP import QuanLySP


class QuanLySPPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        # Màu nền tổng thể
        self.master.configure(bg="#f4f6f9")

        # Kết nối dữ liệu
        self.quanlysp = QuanLySP(
            "database/sanpham.csv",
            ["ma_sp", "ten_sp", "gia", "don_vi", "so_luong"]
        )

        self.current_selected_id = None

        self.view()
        self.load_products()

    def view(self):

        # ================= HEADER =================
        header = tk.Frame(self.master, bg="#d70018", height=85)
        header.pack(fill="x")

        header.pack_propagate(False)

        tk.Label(
            header,
            text="📦 QUẢN LÝ KHO HÀNG WINMART",
            bg="#c30707",
            fg="white",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        # ================= MAIN =================
        main_frame = tk.Frame(self.master, bg="#f4f6f9")
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # ================= THANH TÌM KIẾM =================
        search_frame = tk.Frame(
            main_frame,
            bg="white",
            bd=2,
            relief="groove"
        )
        search_frame.pack(fill="x", pady=10)

        tk.Label(
            search_frame,
            text="🔍 Tìm kiếm sản phẩm:",
            bg="white",
            fg="#333",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10, pady=10)

        self.ent_search = tk.Entry(
            search_frame,
            font=("Arial", 11),
            bd=2,
            relief="groove"
        )

        self.ent_search.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        self.ent_search.bind("<KeyRelease>", self.search_product)

        # ================= KHUNG NHẬP =================
        ifrm = tk.LabelFrame(
            main_frame,
            text=" Thông tin sản phẩm ",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333",
            bd=2,
            relief="groove"
        )

        ifrm.pack(fill="x", pady=10)

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
        tk.Label(ifrm, text="Tên SP:", **label_style).grid(
            row=0, column=0, padx=10, pady=12, sticky="e"
        )

        self.ent_ten = tk.Entry(ifrm, width=25, **entry_style)
        self.ent_ten.grid(row=0, column=1, padx=10, pady=12)

        tk.Label(ifrm, text="Giá bán:", **label_style).grid(
            row=0, column=2, padx=10, pady=12, sticky="e"
        )

        self.ent_gia = tk.Entry(ifrm, width=25, **entry_style)
        self.ent_gia.grid(row=0, column=3, padx=10, pady=12)

        # ===== DÒNG 2 =====
        tk.Label(ifrm, text="Đơn vị:", **label_style).grid(
            row=1, column=0, padx=10, pady=12, sticky="e"
        )

        self.cb_dv = ttk.Combobox(
            ifrm,
            values=["kg", "gói", "chai", "lon", "thùng", "chiếc"],
            state="readonly",
            font=("Arial", 10),
            width=22
        )

        self.cb_dv.grid(row=1, column=1, padx=10, pady=12)
        self.cb_dv.current(0)

        tk.Label(ifrm, text="Số lượng:", **label_style).grid(
            row=1, column=2, padx=10, pady=12, sticky="e"
        )

        self.ent_sl = tk.Entry(ifrm, width=25, **entry_style)
        self.ent_sl.grid(row=1, column=3, padx=10, pady=12)

        # ================= NÚT CHỨC NĂNG =================
        bfrm = tk.Frame(main_frame, bg="#f4f6f9")
        bfrm.pack(pady=15)

        CustomButton(
            bfrm,
            text="➕ Thêm mới",
            command=self.add_product,
            style_type="success",
            width=18
        ).pack(side="left", padx=8)

        CustomButton(
            bfrm,
            text="✏️ Cập nhật",
            command=self.update_product,
            style_type="warning",
            width=18
        ).pack(side="left", padx=8)

        CustomButton(
            bfrm,
            text="🗑️ Xóa hàng",
            command=self.delete_product,
            style_type="danger",
            width=18
        ).pack(side="left", padx=8)

        # QUAY LẠI TRANG CHỦ
        CustomButton(
            bfrm,
            text="⬅ Quay lại Trang chủ",
            command=self.app_manager.show_home_page,
            style_type="secondary",
            width=22
        ).pack(side="left", padx=8)

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
            "Mã SP",
            "Tên sản phẩm",
            "Giá",
            "Đơn vị",
            "Số lượng"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=cols,
            show="headings",
            height=12
        )

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=170, anchor="center")

        # Scrollbar
        scroll_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scroll_y.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # ================= FOOTER =================
        footer = tk.Frame(self.master, bg="#d70018", height=35)
        footer.pack(fill="x", side="bottom")

        tk.Label(
            footer,
            text="WinMart Inventory Management © 2026",
            bg="#d70018",
            fg="white",
            font=("Arial", 9)
        ).pack(pady=7)

    # ================= LOAD DỮ LIỆU =================
    def load_products(self):

        for i in self.tree.get_children():
            self.tree.delete(i)

        res = self.quanlysp.list(1, 1000)
        data = res["data"]

        if hasattr(data, 'values'):
            for item in data.values:
                self.tree.insert("", "end", values=list(item))
        else:
            for item in data:
                self.tree.insert("", "end", values=[
                    item.get("ma_sp"),
                    item.get("ten_sp"),
                    item.get("gia"),
                    item.get("don_vi"),
                    item.get("so_luong")
                ])

    # ================= TÌM KIẾM =================
    def search_product(self, event=None):

        keyword = self.ent_search.get().strip()

        for i in self.tree.get_children():
            self.tree.delete(i)

        res = self.quanlysp.search("ten_sp", keyword)

        if res.empty:
            res = self.quanlysp.search("ma_sp", keyword)

        for _, item in res.iterrows():
            self.tree.insert("", "end", values=list(item))

    # ================= CHỌN DÒNG =================
    def on_tree_select(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        item_data = self.tree.item(selected[0])['values']

        self.current_selected_id = str(item_data[0])

        self.ent_ten.delete(0, 'end')
        self.ent_ten.insert(0, item_data[1])

        self.ent_gia.delete(0, 'end')
        self.ent_gia.insert(0, item_data[2])

        if item_data[3] in self.cb_dv['values']:
            self.cb_dv.set(item_data[3])

        self.ent_sl.delete(0, 'end')
        self.ent_sl.insert(0, item_data[4])

    # ================= THÊM SẢN PHẨM =================
    def add_product(self):

        ten = self.ent_ten.get().strip()
        gia = self.ent_gia.get().strip()
        dv = self.cb_dv.get()
        sl = self.ent_sl.get().strip()

        if not all([ten, gia, sl]):
            messagebox.showwarning(
                "Lỗi",
                "Vui lòng nhập đầy đủ thông tin sản phẩm!"
            )
            return

        check_exist = self.quanlysp.search("ten_sp", ten)

        if not check_exist.empty:
            messagebox.showwarning(
                "Lỗi",
                "Sản phẩm đã tồn tại!"
            )
            return

        ma_sp = f"SP{int(time.time()) % 100000}"

        if self.quanlysp.create([ma_sp, ten, gia, dv, sl]):

            messagebox.showinfo(
                "Thành công",
                f"Đã thêm sản phẩm: {ten}"
            )

            self.load_products()

    # ================= CẬP NHẬT =================
    def update_product(self):

        if not self.current_selected_id:
            messagebox.showwarning(
                "Lỗi",
                "Vui lòng chọn sản phẩm!"
            )
            return

        ten = self.ent_ten.get().strip()
        gia = self.ent_gia.get().strip()
        dv = self.cb_dv.get()
        sl = self.ent_sl.get().strip()

        if not all([ten, gia, sl]):
            messagebox.showwarning(
                "Lỗi",
                "Vui lòng nhập đầy đủ dữ liệu!"
            )
            return

        new_data = [
            self.current_selected_id,
            ten,
            gia,
            dv,
            sl
        ]

        if self.quanlysp.update(
            "ma_sp",
            self.current_selected_id,
            new_data
        ):

            messagebox.showinfo(
                "Thành công",
                "Đã cập nhật sản phẩm!"
            )

            self.load_products()

        else:
            messagebox.showerror(
                "Lỗi",
                "Cập nhật thất bại!"
            )

    # ================= XÓA =================
    def delete_product(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Lỗi",
                "Vui lòng chọn sản phẩm cần xóa!"
            )
            return

        ma_sp = str(
            self.tree.item(selected[0])['values'][0]
        )

        if messagebox.askyesno(
            "Xác nhận",
            f"Bạn có chắc muốn xóa sản phẩm {ma_sp}?"
        ):

            if self.quanlysp.delete("ma_sp", ma_sp):

                messagebox.showinfo(
                    "Thành công",
                    "Đã xóa sản phẩm!"
                )

                self.load_products()