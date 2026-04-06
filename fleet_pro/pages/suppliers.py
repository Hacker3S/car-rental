import customtkinter as ctk
from database.db_handler import get_connection
from components.data_table import DataTable
from components.modal_form import ModalForm

class SuppliersPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="Suppliers", font=ctk.CTkFont(size=28, weight="bold")).pack(side="left")
        ctk.CTkButton(header_frame, text="➕ Add Supplier", command=self.add_supplier).pack(side="right")
        
        self.table = DataTable(self, ["ID", "Name", "Contact", "Cars Supplied"])
        self.table.bind_double_click(self.view_supplied_cars)
        
        self.refresh_data()
        
    def refresh_data(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT s.id, s.name, s.contact, COUNT(c.id) 
                       FROM suppliers s LEFT JOIN cars c ON s.id = c.supplier_id 
                       GROUP BY s.id''')
        self.table.populate(cur.fetchall())
        conn.close()
        
    def add_supplier(self):
        fields = [
            {"label": "Name", "required": True},
            {"label": "Contact", "required": True}
        ]
        
        def save(data):
            conn = get_connection()
            conn.execute("INSERT INTO suppliers (name, contact) VALUES (?, ?)", (data["Name"], data["Contact"]))
            conn.commit()
            conn.close()
            self.refresh_data()
            return True
            
        ModalForm(self, "Add Supplier", fields, save)
        
    def view_supplied_cars(self, event):
        selected = self.table.get_selected()
        if not selected: return
        
        win = ctk.CTkToplevel(self)
        win.title(f"Cars supplied by {selected[1]}")
        win.geometry("500x400")
        win.lift()
        win.attributes("-topmost", True)
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, brand, model, year, status FROM cars WHERE supplier_id=?", (selected[0],))
        rows = cur.fetchall()
        conn.close()
        
        table = DataTable(win, ["ID", "Brand", "Model", "Year", "Status"], allow_selection=False)
        table.pack(fill="both", expand=True, padx=20, pady=20)
        table.populate(rows)
