import tkinter as tk
from tkinter import ttk

class CustomButton(ttk.Button):
    def __init__(self, parent, text="", command=None, style_type="primary", **kwargs):
        self.style_type = style_type
        super().__init__(parent, text=text, command=command, **kwargs)
        self.configure_style()
        
    def configure_style(self):
        style = ttk.Style()
        # Đổi Primary thành màu Đỏ WinMart
        if self.style_type == "primary":
            style.configure('Primary.TButton', font=('Arial', 10, 'bold'), foreground='red')
        elif self.style_type == "success":
            style.configure('Success.TButton', font=('Arial', 10), foreground='green')
        elif self.style_type == "danger":
            style.configure('Danger.TButton', font=('Arial', 10), foreground='red')
        elif self.style_type == "secondary":
            style.configure('Secondary.TButton', font=('Arial', 10), foreground='gray')
        elif self.style_type == "info":
            style.configure('Info.TButton', font=('Arial', 10), foreground='blue')
            
        self.configure(style=f'{self.style_type.capitalize()}.TButton')