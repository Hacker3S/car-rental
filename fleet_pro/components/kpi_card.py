import customtkinter as ctk

class KPICard(ctk.CTkFrame):
    def __init__(self, master, title, value, color="#1F6FEB"):
        super().__init__(master, corner_radius=10)
        
        self.title_label = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=14))
        self.title_label.pack(pady=(10, 0), padx=20, anchor="w")
        
        self.value_label = ctk.CTkLabel(self, text=str(value), text_color=color, font=ctk.CTkFont(size=28, weight="bold"))
        self.value_label.pack(pady=(0, 10), padx=20, anchor="w")
        
    def update_value(self, new_value):
        self.value_label.configure(text=str(new_value))
