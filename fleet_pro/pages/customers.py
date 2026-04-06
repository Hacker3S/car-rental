import customtkinter as ctk
from database.db_handler import get_connection
from components.data_table import DataTable
from components.modal_form import ModalForm

class CustomersPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="Customers", font=ctk.CTkFont(size=28, weight="bold")).pack(side="left")
        ctk.CTkButton(header_frame, text="➕ Register Customer", command=self.add_customer).pack(side="right")
        
        self.table = DataTable(self, ["ID", "Name", "Contact", "License No.", "Total Rentals"])
        
        self.refresh_data()
        
    def refresh_data(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, contact, license_num, total_rentals FROM customers")
        self.table.populate(cur.fetchall())
        conn.close()
        
    def add_customer(self):
        fields = [
            {"label": "Name", "required": True},
            {"label": "Contact", "required": True},
            {"label": "License No.", "required": True}
        ]
        
        def save(data):
            conn = get_connection()
            conn.execute("INSERT INTO customers (name, contact, license_num) VALUES (?, ?, ?)",
                         (data["Name"], data["Contact"], data["License No."]))
            conn.commit()
            conn.close()
            self.refresh_data()
            return True
            
        ModalForm(self, "Register Customer", fields, save)
