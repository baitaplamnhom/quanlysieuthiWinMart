import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import os
from datetime import datetime
from common.button import CustomButton
from query.quanLySP import QuanLySP

class ThanhToanPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        # Kết nối dữ liệu
        self.quanlysp = QuanLySP("database/sanpham.csv", ["ma_sp", "ten_sp", "gia", "don_vi", "so_luong"])
        self.cart = []
        self.total_amount = 0
        self.view()

    def view(self):
        # Header đỏ đặc trưng WinMart
        header = tk.Frame(self.master, bg="#e53935", height=60)
        header.pack(fill="x")
        tk.Label(header, text="WINMART POS - HỆ THỐNG THANH TOÁN", 
                 font=("Arial", 18, "bold"), bg="#e53935", fg="white").pack(pady=10)

        # Container chính
        main_container = tk.Frame(self.master)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # --- CỘT TRÁI: GIỎ HÀNG ---
        left_col = tk.Frame(main_container)
        left_col.place(relx=0, rely=0, relwidth=0.65, relheight=1)

        tk.Label(left_col, text="DANH SÁCH MÓN HÀNG", font=("Arial", 11, "bold")).pack(anchor="w")
        
        cols = ("Mã SP", "Tên sản phẩm", "Giá", "SL", "Thành tiền")
        self.tree_cart = ttk.Treeview(left_col, columns=cols, show="headings")
        for c in cols:
            self.tree_cart.heading(c, text=c)
            self.tree_cart.column(c, anchor="center", width=90)
        self.tree_cart.pack(fill="both", expand=True, pady=5)

        # Khu vực hiển thị tổng tiền to rõ
        summary_frame = tk.Frame(left_col, bg="#f8f9fa", bd=1, relief="solid")
        summary_frame.pack(fill="x", pady=5)
        self.lbl_total = tk.Label(summary_frame, text="TỔNG TIỀN: 0 VNĐ", 
                                 font=("Arial", 22, "bold"), fg="#e53935", bg="#f8f9fa")
        self.lbl_total.pack(pady=10)

        # --- CỘT PHẢI: ĐIỀU KHIỂN ---
        right_col = tk.Frame(main_container, bd=1, relief="solid", bg="#ffffff")
        right_col.place(relx=0.67, rely=0, relwidth=0.33, relheight=1)

        # 1. Ô Tìm kiếm
        tk.Label(right_col, text="TÌM SẢN PHẨM", font=("Arial", 10, "bold"), bg="#ffffff").pack(pady=(10,0))
        self.ent_search = tk.Entry(right_col, font=("Arial", 12))
        self.ent_search.pack(fill="x", padx=15, pady=5)
        self.ent_search.bind("<KeyRelease>", self.search_product)

        # Bảng kết quả tìm kiếm nhanh (chứa Mã SP ẩn để trừ kho)
        self.tree_search = ttk.Treeview(right_col, columns=("Tên", "Giá", "Kho"), show="headings", height=6)
        self.tree_search.heading("Tên", text="Tên SP")
        self.tree_search.heading("Giá", text="Giá")
        self.tree_search.heading("Kho", text="Tồn")
        self.tree_search.column("Tên", width=100)
        self.tree_search.column("Giá", width=60)
        self.tree_search.column("Kho", width=50)
        self.tree_search.pack(fill="x", padx=15, pady=5)
        self.tree_search.bind("<<TreeviewSelect>>", self.on_search_select)

        # 2. Số lượng và Thêm
        tk.Label(right_col, text="SỐ LƯỢNG MUA:", bg="#ffffff").pack(pady=(5,0))
        self.ent_quantity = tk.Entry(right_col, font=("Arial", 12), justify="center")
        self.ent_quantity.pack(fill="x", padx=40, pady=5)
        self.ent_quantity.insert(0, "1")

        CustomButton(right_col, text="THÊM VÀO ĐƠN", command=self.add_to_cart, style_type="success").pack(pady=10)
        
        tk.Frame(right_col, height=1, bg="#dee2e6").pack(fill="x", pady=10, padx=10)

        # 3. Tiền khách đưa & Tiền thừa
        tk.Label(right_col, text="TIỀN KHÁCH ĐƯA:", font=("Arial", 10, "bold"), bg="#ffffff").pack()
        self.ent_customer_money = tk.Entry(right_col, font=("Arial", 14, "bold"), justify="center", fg="#0d6efd")
        self.ent_customer_money.pack(fill="x", padx=25, pady=5)
        self.ent_customer_money.bind("<KeyRelease>", self.calculate_change)

        self.lbl_change = tk.Label(right_col, text="TIỀN THỪA: 0 VNĐ", 
                                  font=("Arial", 12, "bold"), fg="#198754", bg="#ffffff")
        self.lbl_change.pack(pady=10)

        # 4. Nút bấm cuối trang
        CustomButton(right_col, text="XÓA MÓN ĐANG CHỌN", command=self.remove_from_cart, style_type="danger").pack(fill="x", padx=25, pady=5)
        CustomButton(right_col, text="THANH TOÁN & IN HD", command=self.process_checkout, style_type="warning").pack(fill="x", padx=25, pady=5)
        CustomButton(right_col, text="QUAY LẠI TRANG CHỦ", command=self.app_manager.show_home_page, style_type="secondary").pack(fill="x", padx=25, pady=15)

    def search_product(self, event=None):
        keyword = self.ent_search.get().strip()
        for i in self.tree_search.get_children(): self.tree_search.delete(i)
        if not keyword: return
        
        res = self.quanlysp.search("ten_sp", keyword)
        if res.empty: res = self.quanlysp.search("ma_sp", keyword)
        
        for _, item in res.iterrows():
            # Cột index 3 là Mã SP (quan trọng để trừ kho)
            self.tree_search.insert("", "end", values=[item['ten_sp'], int(item['gia']), item['so_luong'], str(item['ma_sp']), item['don_vi']])

    def on_search_select(self, event=None):
        selected = self.tree_search.selection()
        if not selected: return
        vals = self.tree_search.item(selected[0])['values']
        # Lưu dữ liệu vào biến tạm, đảm bảo mã SP là String
        self.temp_sp_data = {
            'ten': vals[0], 'gia': float(vals[1]), 'kho': int(vals[2]), 'ma': str(vals[3]), 'dv': vals[4]
        }

    def add_to_cart(self):
        if not hasattr(self, 'temp_sp_data'):
            messagebox.showwarning("Lỗi", "Vui lòng chọn một sản phẩm từ danh sách!")
            return
        qty_str = self.ent_quantity.get()
        if not qty_str.isdigit() or int(qty_str) <= 0: return
        qty = int(qty_str)
        
        if qty > self.temp_sp_data['kho']:
            messagebox.showwarning("Lỗi", "Số lượng trong kho không đủ!")
            return

        # Kiểm tra trùng trong giỏ
        for item in self.cart:
            if item['ma_sp'] == self.temp_sp_data['ma']:
                item['so_luong'] += qty
                item['thanh_tien'] = item['so_luong'] * item['gia']
                self.update_cart_view()
                return

        self.cart.append({
            'ma_sp': self.temp_sp_data['ma'], 'ten_sp': self.temp_sp_data['ten'],
            'gia': self.temp_sp_data['gia'], 'so_luong': qty, 'thanh_tien': qty * self.temp_sp_data['gia']
        })
        self.update_cart_view()

    def remove_from_cart(self):
        selected = self.tree_cart.selection()
        if not selected: return
        ma_sp_del = str(self.tree_cart.item(selected[0])['values'][0])
        self.cart = [i for i in self.cart if str(i['ma_sp']) != ma_sp_del]
        self.update_cart_view()

    def update_cart_view(self):
        for i in self.tree_cart.get_children(): self.tree_cart.delete(i)
        self.total_amount = sum(i['thanh_tien'] for i in self.cart)
        for i in self.cart:
            self.tree_cart.insert("", "end", values=[i['ma_sp'], i['ten_sp'], int(i['gia']), i['so_luong'], int(i['thanh_tien'])])
        self.lbl_total.config(text=f"TỔNG TIỀN: {int(self.total_amount):,} VNĐ")
        self.calculate_change()

    def calculate_change(self, event=None):
        money_str = self.ent_customer_money.get().strip()
        if not money_str.isdigit(): 
            self.lbl_change.config(text="TIỀN THỪA: 0 VNĐ", fg="black")
            return
        change = int(money_str) - self.total_amount
        if change >= 0:
            self.lbl_change.config(text=f"TIỀN THỪA: {int(change):,} VNĐ", fg="#198754")
        else:
            self.lbl_change.config(text=f"THIẾU: {int(abs(change)):,} VNĐ", fg="#dc3545")

    def process_checkout(self):
        if not self.cart: 
            messagebox.showwarning("Lỗi", "Giỏ hàng đang trống!")
            return
        money_str = self.ent_customer_money.get().strip()
        if not money_str.isdigit() or int(money_str) < self.total_amount:
            messagebox.showerror("Lỗi", "Tiền khách đưa chưa đủ!")
            return

        try:
            # 1. TRỪ KHO CHÍNH XÁC
            df_sp = pd.read_csv("database/sanpham.csv")
            df_sp['ma_sp'] = df_sp['ma_sp'].astype(str) # Ép kiểu về String để so khớp

            for item in self.cart:
                ma_mua = str(item['ma_sp'])
                idx = df_sp.index[df_sp['ma_sp'] == ma_mua].tolist()
                if idx:
                    df_sp.at[idx[0], 'so_luong'] -= int(item['so_luong'])
            
            df_sp.to_csv("database/sanpham.csv", index=False)

            # 2. IN HÓA ĐƠN FILE .TXT
            hd_code = datetime.now().strftime("%Y%m%d%H%M%S")
            os.makedirs("hoadon", exist_ok=True)
            file_path = f"hoadon/HD_{hd_code}.txt"
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("      WINMART - HOA DON THANH TOAN      \n")
                f.write(f" Ngay: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write(f" Ma HD: HD_{hd_code}\n")
                f.write("-" * 40 + "\n")
                for i in self.cart:
                    line = f"{i['ten_sp'][:15]:<15} x{i['so_luong']:<3} {int(i['thanh_tien']):>15,}\n"
                    f.write(line)
                f.write("-" * 40 + "\n")
                f.write(f" TONG CONG: {int(self.total_amount):>25,} VND\n")
                f.write(f" KHACH ĐƯA: {int(money_str):>25,} VND\n")
                f.write(f" TIEN THUA: {int(int(money_str)-self.total_amount):>25,} VND\n")
                f.write("-" * 40 + "\n")
                f.write("      CAM ON QUY KHACH - HEN GAP LAI!     ")

            messagebox.showinfo("Thành công", f"Đã thanh toán & trừ kho!\nHóa đơn HD_{hd_code}.txt đã được xuất.")
            
            # Reset
            self.cart = []
            self.update_cart_view()
            self.ent_customer_money.delete(0, 'end')
            self.ent_search.delete(0, 'end')
            for i in self.tree_search.get_children(): self.tree_search.delete(i)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi hệ thống: {e}")