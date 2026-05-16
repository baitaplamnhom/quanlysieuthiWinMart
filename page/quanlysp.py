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
        # Khởi tạo lớp kết nối dữ liệu với 5 thuộc tính chính của sản phẩm
        self.quanlysp = QuanLySP("database/sanpham.csv", ["ma_sp", "ten_sp", "gia", "don_vi", "so_luong"])
        self.current_selected_id = None  # Biến lưu mã sản phẩm đang chọn để phục vụ chức năng Sửa
        self.view()
        self.load_products()

    def view(self):
        # --- Tiêu đề trang ---
        tk.Label(self.master, text="QUẢN LÝ KHO HÀNG WINMART", 
                 font=("Arial", 20, "bold"), fg="#e53935").pack(pady=10)

        # --- THANH TÌM KIẾM SẢN PHẨM (MỚI) ---
        search_frame = tk.Frame(self.master)
        search_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(search_frame, text="Tìm kiếm sản phẩm (Tên/Mã):", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.ent_search = tk.Entry(search_frame, font=("Arial", 11))
        self.ent_search.pack(side="left", fill="x", expand=True, padx=5)
        self.ent_search.bind("<KeyRelease>", self.search_product)  # Gõ ký tự nào tự động lọc ký tự đó

        # --- Khung Nhập thông tin sản phẩm ---
        ifrm = tk.LabelFrame(self.master, text="Thông tin sản phẩm")
        ifrm.pack(fill="x", padx=20, pady=10)

        # Dòng 1: Tên & Giá
        tk.Label(ifrm, text="Tên SP:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_ten = tk.Entry(ifrm, font=("Arial", 11))
        self.ent_ten.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(ifrm, text="Giá bán:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_gia = tk.Entry(ifrm, font=("Arial", 11))
        self.ent_gia.grid(row=0, column=3, padx=5, pady=5)

        # Dòng 2: Đơn vị & Số lượng
        tk.Label(ifrm, text="Đơn vị:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.cb_dv = ttk.Combobox(ifrm, values=["kg", "gói", "chai", "lon", "thùng", "chiếc"], state="readonly")
        self.cb_dv.grid(row=1, column=1, padx=5, pady=5)
        self.cb_dv.current(0)

        tk.Label(ifrm, text="Số lượng:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_sl = tk.Entry(ifrm, font=("Arial", 11))
        self.ent_sl.grid(row=1, column=3, padx=5, pady=5)

        # --- Khung Nút chức năng (Thêm/Sửa/Xóa/Làm mới chữ) ---
        bfrm = tk.Frame(self.master)
        bfrm.pack(pady=10)

        CustomButton(bfrm, text="Thêm mới", command=self.add_product, style_type="success").pack(side="left", padx=5)
        CustomButton(bfrm, text="Cập nhật (Sửa)", command=self.update_product, style_type="warning").pack(side="left", padx=5)
        CustomButton(bfrm, text="Xóa hàng", command=self.delete_product, style_type="danger").pack(side="left", padx=5)
        CustomButton(bfrm, text="Xóa chữ nhập", command=self.clear_entries, style_type="info").pack(side="left", padx=5)

        # --- Bảng hiển thị danh sách sản phẩm (Treeview) ---
        cols = ("Mã SP", "Tên sản phẩm", "Giá", "Đơn vị", "Số lượng")
        self.tree = ttk.Treeview(self.master, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Bắt sự kiện click chọn dòng trên bảng Treeview để đẩy ngược dữ liệu lên form
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # --- NÚT QUAY LẠI TRANG CHỦ (Đặt ở vị trí dưới cùng, căn giữa) ---
        CustomButton(self.master, text="Quay lại Trang chủ", 
                     command=self.app_manager.show_home_page, 
                     style_type="secondary").pack(pady=20)

    def load_products(self):
        """Làm trống bảng và nạp lại toàn bộ dữ liệu mới từ file CSV sản phẩm"""
        for i in self.tree.get_children(): 
            self.tree.delete(i)
        res = self.quanlysp.list(1, 1000)
        data = res["data"]
        if hasattr(data, 'values'):  # Kiểm tra nếu data là một DataFrame của Pandas
            for item in data.values: 
                self.tree.insert("", "end", values=list(item))
        else:  # Trường hợp data là dạng danh sách các dict thông thường
            for item in data:
                self.tree.insert("", "end", values=[
                    item.get("ma_sp"), item.get("ten_sp"), 
                    item.get("gia"), item.get("don_vi"), item.get("so_luong")
                ])

    def search_product(self, event=None):
        """Tìm kiếm dữ liệu tức thì khi người dùng gõ phím"""
        keyword = self.ent_search.get().strip()
        for i in self.tree.get_children(): 
            self.tree.delete(i)
        
        # Tìm kiếm theo tên sản phẩm trước
        res = self.quanlysp.search("ten_sp", keyword)
        
        # Nếu tìm theo tên không có kết quả, thử tìm theo mã sản phẩm
        if res.empty:
            res = self.quanlysp.search("ma_sp", keyword)
            
        for _, item in res.iterrows():
            self.tree.insert("", "end", values=list(item))

    def on_tree_select(self, event=None):
        """Đẩy thông tin của dòng sản phẩm được chọn lên các ô Entry để chỉnh sửa"""
        selected = self.tree.selection()
        if not selected: 
            return
        item_data = self.tree.item(selected[0])['values']
        
        # Lưu lại mã sản phẩm của dòng đang click chọn
        self.current_selected_id = str(item_data[0])
        
        # Điền dữ liệu text vào form nhập liệu
        self.ent_ten.delete(0, 'end'); self.ent_ten.insert(0, item_data[1])
        self.ent_gia.delete(0, 'end'); self.ent_gia.insert(0, item_data[2])
        
        # Chọn mục đơn vị tương ứng trong combobox
        if item_data[3] in self.cb_dv['values']:
            self.cb_dv.set(item_data[3])
            
        self.ent_sl.delete(0, 'end'); self.ent_sl.insert(0, item_data[4])

    def add_product(self):
        """Thêm sản phẩm mới với mã sản phẩm tự tạo theo thời gian thực tế"""
        ten = self.ent_ten.get().strip()
        gia = self.ent_gia.get().strip()
        dv = self.cb_dv.get()
        sl = self.ent_sl.get().strip()
        
        if not all([ten, gia, sl]):
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin sản phẩm mới!")
            return
        
        # Ngăn chặn việc thêm trùng tên sản phẩm đã có sẵn trong kho
        check_exist = self.quanlysp.search("ten_sp", ten)
        if not check_exist.empty:
            messagebox.showwarning("Lỗi", "Sản phẩm này đã tồn tại! Vui lòng chọn sản phẩm trong bảng và bấm nút Sửa để tăng số lượng.")
            return

        # Tạo mã ngẫu nhiên SPxxxxx không bị trùng bằng thời gian chạy hệ thống
        ma_sp = f"SP{int(time.time()) % 100000}"
        if self.quanlysp.create([ma_sp, ten, gia, dv, sl]):
            messagebox.showinfo("Thành công", f"Đã thêm mới thành công sản phẩm: {ten}")
            self.load_products()
            self.clear_entries()

    def update_product(self):
        """Cập nhật thông tin mới vào đúng vị trí dòng dữ liệu cũ trong file CSV"""
        if not self.current_selected_id:
            messagebox.showwarning("Lỗi", "Vui lòng click chọn một sản phẩm từ bảng bên dưới trước khi thực hiện sửa!")
            return
            
        ten = self.ent_ten.get().strip()
        gia = self.ent_gia.get().strip()
        dv = self.cb_dv.get()
        sl = self.ent_sl.get().strip()
        
        if not all([ten, gia, sl]):
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ dữ liệu mới để chỉnh sửa!")
            return
            
        new_data = [self.current_selected_id, ten, gia, dv, sl]
        
        if self.quanlysp.update("ma_sp", self.current_selected_id, new_data):
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin sản phẩm thành công vào cơ sở dữ liệu!")
            self.load_products()
            self.clear_entries()
        else:
            messagebox.showerror("Lỗi", "Cập nhật dữ liệu thất bại!")

    def delete_product(self):
        """Xóa sản phẩm được chọn ra khỏi danh sách bảng và file lưu trữ"""
        selected = self.tree.selection()
        if not selected: 
            messagebox.showwarning("Lỗi", "Vui lòng click chọn sản phẩm cần xóa trong bảng dữ liệu!")
            return
        ma_sp = str(self.tree.item(selected[0])['values'][0])
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa vĩnh viễn sản phẩm có mã {ma_sp}?"):
            if self.quanlysp.delete("ma_sp", ma_sp):
                messagebox.showinfo("Thành công", "Đã xóa sản phẩm khỏi kho hàng thành công!")
                self.load_products()
                self.clear_entries()

    def clear_entries(self):
        """Xóa trắng toàn bộ các ô nhập dữ liệu và reset biến tạm thời đang chọn dòng"""
        self.ent_ten.delete(0, 'end')
        self.ent_gia.delete(0, 'end')
        self.ent_sl.delete(0, 'end')
        self.ent_search.delete(0, 'end')
        self.cb_dv.current(0)
        self.current_selected_id = None