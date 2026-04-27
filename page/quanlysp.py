import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import time
from common.button import CustomButton
from query.quanLySP import QuanLySP

class QuanLySPPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.db_path = "database/sanpham.csv"
        self.quanlysp = QuanLySP("database/sanpham.csv",["ma_sp","ten_sp","gia","don_vi","so_luong"])
        self.view()
        self.load_products()

    def view(self):
        tk.Label(self.master, text="QUẢN LÝ KHO WINMART", font=("Arial", 20, "bold"), fg="red").pack(pady=10)

        # Frame Nhập liệu
        ifrm = tk.LabelFrame(self.master, text="Nhập hàng hóa")
        ifrm.pack(fill="x", padx=20, pady=10)

        tk.Label(ifrm, text="Tên SP:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_ten = tk.Entry(ifrm); self.ent_ten.grid(row=0, column=1)

        tk.Label(ifrm, text="Giá:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_gia = tk.Entry(ifrm); self.ent_gia.grid(row=0, column=3)

        tk.Label(ifrm, text="Đơn vị:").grid(row=1, column=0, padx=5, pady=5)
        self.cb_dv = ttk.Combobox(ifrm, values=["kg", "bó", "gói"]); self.cb_dv.grid(row=1, column=1)

        tk.Label(ifrm, text="Số lượng:").grid(row=1, column=2, padx=5, pady=5)
        self.ent_sl = tk.Entry(ifrm); self.ent_sl.grid(row=1, column=3)

        # Nút bấm
        bfrm = tk.Frame(self.master)
        bfrm.pack(pady=10)
        CustomButton(bfrm, text="Thêm hàng", command=self.add_product, style_type="success").pack(side="left", padx=5)
        CustomButton(bfrm, text="Xóa hàng", command=self.delete_product, style_type="danger").pack(side="left", padx=5)
        CustomButton(bfrm, text="Đăng xuất", command=self.app_manager.show_login_page, style_type="secondary").pack(side="left", padx=5)

        # Bảng dữ liệu
        cols = ("ID", "Tên", "Giá", "Đơn vị", "Số lượng")
        self.tree = ttk.Treeview(self.master, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def load_products(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        data  = self.quanlysp.list(1,10000)
        for item in data["data"]:
            self.tree.insert("", "end", values=[item["ma_sp"],item["ten_sp"],item["gia"],item["don_vi"],item["so_luong"]])

    def add_product(self):
        data = [f"WM{int(time.time())%1000}", self.ent_ten.get(), self.ent_gia.get(), self.cb_dv.get(), self.ent_sl.get()]
        if not all(data[1:]): return messagebox.showwarning("Lỗi", "Nhập đủ thông tin!")
        
        self.quanlysp.create(data)
        self.load_products()
        messagebox.showinfo("Xong", "Đã nhập hàng thành công!")

    def delete_product(self):
        sel = self.tree.selection()
        if not sel: return
        ma = self.tree.item(sel[0], "values")[0]
        self.quanlysp.delete("ma_sp",ma)
        self.load_products()