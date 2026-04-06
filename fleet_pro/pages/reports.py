import customtkinter as ctk
from database.db_handler import get_connection
from utils.pdf_exporter import export_table_to_pdf
import os

class ReportsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        header = ctk.CTkLabel(self, text="Reports", font=ctk.CTkFont(size=28, weight="bold"))
        header.pack(anchor="w", pady=(0, 20))
        
        self.report_type = ctk.CTkComboBox(self, values=["All Transactions", "Available Fleet", "Customer Activity"])
        self.report_type.pack(anchor="w", pady=10)
        
        ctk.CTkButton(self, text="Generate PDF Report", command=self.generate).pack(anchor="w")
        
        self.status_lbl = ctk.CTkLabel(self, text="")
        self.status_lbl.pack(anchor="w", pady=10)
        
    def generate(self):
        conn = get_connection()
        cur = conn.cursor()
        rtype = self.report_type.get()
        
        if rtype == "All Transactions":
            cur.execute("SELECT id, customer_id, car_id, start_date, end_date, total_cost, status FROM transactions")
            cols = ["ID", "Customer ID", "Car ID", "Start", "End", "Cost", "Status"]
            data = cur.fetchall()
            
        elif rtype == "Available Fleet":
            cur.execute("SELECT id, brand, model, year, price_per_day FROM cars WHERE status='Available'")
            cols = ["ID", "Brand", "Model", "Year", "Price/Day"]
            data = cur.fetchall()
            
        elif rtype == "Customer Activity":
            cur.execute("SELECT id, name, total_rentals FROM customers ORDER BY total_rentals DESC")
            cols = ["ID", "Name", "Total Rentals"]
            data = cur.fetchall()
            
        conn.close()
        
        path = export_table_to_pdf(f"{rtype} Report", cols, data)
        abs_path = os.path.abspath(path)
        self.status_lbl.configure(text=f"✅ Report saved to {abs_path}", text_color="green")
