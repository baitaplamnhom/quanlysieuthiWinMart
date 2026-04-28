import tkinter as tk
from tkinter import messagebox, ttk
from common.button import CustomButton
from query.quanLySP import QuanLySP
import pandas as pd

class ThanhToanPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        # Dùng QuanLySP để lấy dữ liệu sản phẩm phục vụ bán hàng
        self.quanlysp = QuanLySP("database/sanpham.csv", ["ma_sp", "ten_sp", "gia", "don_vi", "so_luong"])
        self.gio_hang = [] # Danh sách lưu các mặt hàng khách chọn
        self.view()

    def view(self):
        # Tiêu đề
        tk.Label(self.master, text="HỆ THỐNG THANH TOÁN WINMART", font=("Arial", 20, "bold"), fg="#e53935").pack(pady=10)

        # --- Frame chính chia làm 2 cột ---
        main_container = tk.Frame(self.master)
        main_container.pack(fill="both", expand=True, padx=20)

        # CỘT TRÁI: Tìm kiếm và chọn sản phẩm
        left_frame = tk.LabelFrame(main_container, text="Chọn sản phẩm", padx=10, pady=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left_frame, text="Nhập mã hoặc tên SP:").pack(anchor="w")
        self.ent_search = tk.Entry(left_frame, font=("Arial", 12))
        self.ent_search.pack(fill="x", pady=5)
        self.ent_search.bind("<KeyRelease>", self.search_sp) # Tìm kiếm ngay khi gõ

        # Bảng danh sách sản phẩm trong kho để chọn
        self.tree_sp = ttk.Treeview(left_frame, columns=("ID", "Tên", "Giá", "Kho"), show="headings", height=10)
        self.tree_sp.heading("ID", text="Mã"); self.tree_sp.column("ID", width=60)
        self.tree_sp.heading("Tên", text="Tên SP"); self.tree_sp.column("Tên", width=150)
        self.tree_sp.heading("Giá", text="Giá"); self.tree_sp.column("Giá", width=80)
        self.tree_sp.heading("Kho", text="Kho"); self.tree_sp.column("Kho", width=50)
        self.tree_sp.pack(fill="both", expand=True, pady=5)

        tk.Label(left_frame, text="Số lượng mua:").pack(anchor="w")
        self.ent_sl_mua = tk.Entry(left_frame, font=("Arial", 12))
        self.ent_sl_mua.insert(0, "1") # Mặc định là 1
        self.ent_sl_mua.pack(fill="x", pady=5)

        CustomButton(left_frame, text="Thêm vào giỏ hàng", command=self.add_to_cart, style_type="success").pack(fill="x", pady=10)

        # CỘT PHẢI: Giỏ hàng và Thanh toán
        right_frame = tk.LabelFrame(main_container, text="Giỏ hàng hiện tại", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)

        self.tree_cart = ttk.Treeview(right_frame, columns=("Tên", "SL", "Đơn giá", "Thành tiền"), show="headings")
        self.tree_cart.heading("Tên", text="Tên SP")
        self.tree_cart.heading("SL", text="SL"); self.tree_cart.column("SL", width=40)
        self.tree_cart.heading("Đơn giá", text="Đơn giá")
        self.tree_cart.heading("Thành tiền", text="T.Tiền")
        self.tree_cart.pack(fill="both", expand=True)

        self.lbl_tong_tien = tk.Label(right_frame, text="TỔNG: 0 VNĐ", font=("Arial", 16, "bold"), fg="blue")
        self.lbl_tong_tien.pack(pady=10)

        btn_group = tk.Frame(right_frame)
        btn_group.pack(fill="x")

        CustomButton(btn_group, text="THANH TOÁN", command=self.checkout, style_type="primary").pack(side="left", expand=True, padx=5)
        CustomButton(btn_group, text="Xóa món", command=self.remove_from_cart, style_type="danger").pack(side="left", expand=True, padx=5)
        
        # Nút quay lại trang chủ
        CustomButton(self.master, text="Quay lại Trang chủ", command=self.app_manager.show_home_page, style_type="secondary").pack(pady=10)

        self.load_all_sp()

    def load_all_sp(self):
        for i in self.tree_sp.get_children(): self.tree_sp.delete(i)
        res = self.quanlysp.list(1, 1000)
        for item in res["data"]:
            self.tree_sp.insert("", "end", values=[item["ma_sp"], item["ten_sp"], item["gia"], item["so_luong"]])

    def search_sp(self, event=None):
        keyword = self.ent_search.get()
        # Tìm kiếm trong tên hoặc mã
        res = self.quanlysp.search("ten_sp", keyword)
        for i in self.tree_sp.get_children(): self.tree_sp.delete(i)
        for _, item in res.iterrows():
            self.tree_sp.insert("", "end", values=[item["ma_sp"], item["ten_sp"], item["gia"], item["so_luong"]])

    def add_to_cart(self):
        selected = self.tree_sp.selection()
        if not selected:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một sản phẩm từ danh sách!")
            return
        
        try:
            sl_mua = int(self.ent_sl_mua.get())
            if sl_mua <= 0: raise ValueError
        except:
            messagebox.showwarning("Lỗi", "Số lượng mua phải là số nguyên dương!")
            return

        item = self.tree_sp.item(selected[0])['values']
        ma_sp, ten, gia, kho = item[0], item[1], int(item[2]), int(item[3])

        if sl_mua > kho:
            messagebox.showerror("Lỗi", f"Trong kho chỉ còn {kho} sản phẩm!")
            return

        thanh_tien = sl_mua * gia
        self.gio_hang.append({"ma_sp": ma_sp, "ten": ten, "sl": sl_mua, "gia": gia, "thanh_tien": thanh_tien})
        self.update_cart_view()

    def update_cart_view(self):
        for i in self.tree_cart.get_children(): self.tree_cart.delete(i)
        tong = 0
        for item in self.gio_hang:
            self.tree_cart.insert("", "end", values=[item["ten"], item["sl"], item["gia"], item["thanh_tien"]])
            tong += item["thanh_tien"]
        self.lbl_tong_tien.config(text=f"TỔNG: {tong:,} VNĐ")

    def remove_from_cart(self):
        selected = self.tree_cart.selection()
        if not selected: return
        idx = self.tree_cart.index(selected[0])
        del self.gio_hang[idx]
        self.update_cart_view()

    def checkout(self):
        if not self.gio_hang:
            messagebox.showwarning("Lỗi", "Giỏ hàng đang trống!")
            return

        if messagebox.askyesno("Xác nhận", "Xác nhận thanh toán và in hóa đơn?"):
            # Cập nhật số lượng trong kho
            df_sp = pd.read_csv("database/sanpham.csv")
            for item in self.gio_hang:
                # Trừ số lượng trong DataFrame
                df_sp.loc[df_sp['ma_sp'].astype(str) == str(item['ma_sp']), 'so_luong'] -= item['sl']
            
            # Lưu lại vào file CSV
            df_sp.to_csv("database/sanpham.csv", index=False)
            
            messagebox.showinfo("Thành công", "Thanh toán hoàn tất! Kho hàng đã được cập nhật.")
            self.gio_hang = []
            self.update_cart_view()
            self.load_all_sp() # Cập nhật lại danh sách kho bên trái