import tkinter as tk
from tkinter import messagebox, ttk
import time
from common.button import CustomButton
from query.quanLySP import QuanLySP

class QuanLySPPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.quanlysp = QuanLySP("database/sanpham.csv", ["ma_sp", "ten_sp", "gia", "don_vi", "so_luong"])
        self.view()
        self.load_products()

    def view(self):
        tk.Label(self.master, text="QUẢN LÝ KHO HÀNG WINMART", 
                 font=("Arial", 20, "bold"), fg="#e53935").pack(pady=10)

        # --- Frame Nhập liệu ---
        ifrm = tk.LabelFrame(self.master, text="Thông tin sản phẩm")
        ifrm.pack(fill="x", padx=20, pady=10)

        tk.Label(ifrm, text="Tên SP:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_ten = tk.Entry(ifrm, font=("Arial", 11))
        self.ent_ten.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ifrm, text="Giá bán:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_gia = tk.Entry(ifrm, font=("Arial", 11))
        self.ent_gia.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(ifrm, text="Đơn vị:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.cb_dv = ttk.Combobox(ifrm, values=["kg", "gói", "chai", "lon", "thùng", "chiếc"], state="readonly")
        self.cb_dv.grid(row=1, column=1, padx=5, pady=5)
        self.cb_dv.current(0)

        tk.Label(ifrm, text="Số lượng:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_sl = tk.Entry(ifrm, font=("Arial", 11))
        self.ent_sl.grid(row=1, column=3, padx=5, pady=5)

        # --- Frame Nút chức năng (Thêm/Xóa) ---
        bfrm = tk.Frame(self.master)
        bfrm.pack(pady=10)

        CustomButton(bfrm, text="Thêm hàng", command=self.add_product, style_type="success").pack(side="left", padx=5)
        CustomButton(bfrm, text="Xóa hàng", command=self.delete_product, style_type="danger").pack(side="left", padx=5)

        # --- Bảng hiển thị (Treeview) ---
        cols = ("Mã SP", "Tên sản phẩm", "Giá", "Đơn vị", "Số lượng")
        self.tree = ttk.Treeview(self.master, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # --- NÚT QUAY LẠI (Đặt dưới cùng giống trang thanh toán) ---
        CustomButton(self.master, text="Quay lại Trang chủ", 
                     command=self.app_manager.show_home_page, 
                     style_type="secondary").pack(pady=20)

    def load_products(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        res = self.quanlysp.list(1, 1000)
        data = res["data"]
        if hasattr(data, 'values'):
            for item in data.values: self.tree.insert("", "end", values=list(item))
        else:
            for item in data:
                self.tree.insert("", "end", values=[item.get("ma_sp"), item.get("ten_sp"), item.get("gia"), item.get("don_vi"), item.get("so_luong")])

    def add_product(self):
        ten, gia, dv, sl = self.ent_ten.get(), self.ent_gia.get(), self.cb_dv.get(), self.ent_sl.get()
        if not all([ten, gia, sl]):
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        ma_sp = f"SP{int(time.time()) % 100000}"
        if self.quanlysp.create([ma_sp, ten, gia, dv, sl]):
            messagebox.showinfo("Thành công", f"Đã thêm: {ten}")
            self.load_products()
            self.clear_entries()

    def delete_product(self):
        selected = self.tree.selection()
        if not selected: return
        ma_sp = str(self.tree.item(selected[0])['values'][0])
        if messagebox.askyesno("Xác nhận", f"Xóa mã hàng {ma_sp}?"):
            if self.quanlysp.delete("ma_sp", ma_sp):
                self.load_products()

    def clear_entries(self):
        self.ent_ten.delete(0, 'end'); self.ent_gia.delete(0, 'end'); self.ent_sl.delete(0, 'end')
        