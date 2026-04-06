import customtkinter as ctk
from database.db_handler import get_connection
from components.data_table import DataTable
from components.modal_form import ModalForm

class FleetPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="Fleet Management", font=ctk.CTkFont(size=28, weight="bold")).pack(side="left")
        
        ctk.CTkButton(header_frame, text="➕ Add Car", command=self.add_car).pack(side="right", padx=5)
        ctk.CTkButton(header_frame, text="✏️ Edit", command=self.edit_car).pack(side="right", padx=5)
        ctk.CTkButton(header_frame, text="🔧 Maint.", command=self.mark_maintenance).pack(side="right", padx=5)
        ctk.CTkButton(header_frame, text="🗑️ Delete", fg_color="#E74C3C", hover_color="#C0392B", command=self.delete_car).pack(side="right", padx=5)
        
        filter_frame = ctk.CTkFrame(self, corner_radius=10)
        filter_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(filter_frame, text="Filter Category:").pack(side="left", padx=10, pady=10)
        self.cat_filter = ctk.CTkComboBox(filter_frame, values=["All", "Sedan", "SUV", "Luxury"], command=self.refresh_data)
        self.cat_filter.pack(side="left", padx=10)
        
        ctk.CTkLabel(filter_frame, text="Filter Status:").pack(side="left", padx=10, pady=10)
        self.stat_filter = ctk.CTkComboBox(filter_frame, values=["All", "Available", "Rented", "Maintenance"], command=self.refresh_data)
        self.stat_filter.pack(side="left", padx=10)
        
        self.table = DataTable(self, ["ID", "Brand", "Model", "Year", "Category", "Price/Day", "Mileage", "Supplier", "Status"])
        
        self.refresh_data()
        
    def refresh_data(self, _=None):
        conn = get_connection()
        cur = conn.cursor()
        
        query = '''SELECT c.id, c.brand, c.model, c.year, c.category, c.price_per_day, 
                   c.mileage, s.name, c.status 
                   FROM cars c LEFT JOIN suppliers s ON c.supplier_id = s.id WHERE 1=1'''
        params = []
        
        cat = self.cat_filter.get()
        if cat != "All":
            query += " AND category=?"
            params.append(cat)
            
        stat = self.stat_filter.get()
        if stat != "All":
            query += " AND status=?"
            params.append(stat)
            
        cur.execute(query, params)
        self.table.populate(cur.fetchall())
        conn.close()
        
    def add_car(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM suppliers")
        sups = [f"{r[0]} - {r[1]}" for r in cur.fetchall()]
        conn.close()
        
        fields = [
            {"label": "Brand", "required": True},
            {"label": "Model", "required": True},
            {"label": "Year", "required": True, "numeric": True},
            {"label": "Category", "type": "dropdown", "options": ["Sedan", "SUV", "Luxury"]},
            {"label": "Price/Day", "required": True, "numeric": True},
            {"label": "Mileage", "required": True, "numeric": True},
            {"label": "Supplier", "type": "dropdown", "options": sups if sups else ["None"]}
        ]
        
        def save(data):
            conn = get_connection()
            cur = conn.cursor()
            sup_id = data["Supplier"].split(" - ")[0] if data["Supplier"] != "None" else None
            
            cur.execute('''INSERT INTO cars (brand, model, year, category, price_per_day, mileage, supplier_id, status)
                           VALUES (?, ?, ?, ?, ?, ?, ?, 'Available')''', 
                        (data["Brand"], data["Model"], data["Year"], data["Category"], 
                         data["Price/Day"], data["Mileage"], sup_id))
            conn.commit()
            conn.close()
            self.refresh_data()
            return True
            
        ModalForm(self, "Add New Car", fields, save)
        
    def edit_car(self):
        selected = self.table.get_selected()
        if not selected:
            return
            
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM suppliers")
        sups = [f"{r[0]} - {r[1]}" for r in cur.fetchall()]
        conn.close()
        
        fields = [
            {"label": "Brand", "default": selected[1], "required": True},
            {"label": "Model", "default": selected[2], "required": True},
            {"label": "Year", "default": selected[3], "required": True, "numeric": True},
            {"label": "Category", "type": "dropdown", "options": ["Sedan", "SUV", "Luxury"], "default": selected[4]},
            {"label": "Price/Day", "default": selected[5], "required": True, "numeric": True},
            {"label": "Mileage", "default": selected[6], "required": True, "numeric": True},
            {"label": "Supplier", "type": "dropdown", "options": sups if sups else ["None"]} 
        ]
        
        def save(data):
            conn = get_connection()
            cur = conn.cursor()
            sup_id = data["Supplier"].split(" - ")[0] if data["Supplier"] != "None" else None
            
            cur.execute('''UPDATE cars SET brand=?, model=?, year=?, category=?, price_per_day=?, mileage=?, supplier_id=?
                           WHERE id=?''', 
                        (data["Brand"], data["Model"], data["Year"], data["Category"], 
                         data["Price/Day"], data["Mileage"], sup_id, selected[0]))
            conn.commit()
            conn.close()
            self.refresh_data()
            return True
            
        ModalForm(self, "Edit Car", fields, save)
        
    def mark_maintenance(self):
        selected = self.table.get_selected()
        if not selected: return
        conn = get_connection()
        conn.execute("UPDATE cars SET status='Maintenance' WHERE id=?", (selected[0],))
        conn.commit()
        conn.close()
        self.refresh_data()
        
    def delete_car(self):
        selected = self.table.get_selected()
        if not selected: return
        from CTkMessagebox import CTkMessagebox
        msg = CTkMessagebox(title="Delete Car?", message=f"Are you sure you want to delete {selected[1]} {selected[2]}?",
                            icon="warning", option_1="Cancel", option_2="Delete")
        if msg.get() == "Delete":
            conn = get_connection()
            conn.execute("DELETE FROM cars WHERE id=?", (selected[0],))
            conn.commit()
            conn.close()
            self.refresh_data()
