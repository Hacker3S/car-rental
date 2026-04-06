import customtkinter as ctk
from database.db_handler import get_connection
from components.data_table import DataTable
from components.modal_form import ModalForm
from tkcalendar import DateEntry
from datetime import datetime

class BookingsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        
        self.tab_active = self.tabview.add("Active Rentals")
        self.tab_all = self.tabview.add("All Transactions")
        
        hdr1 = ctk.CTkFrame(self.tab_active, fg_color="transparent")
        hdr1.pack(fill="x", pady=(0, 10))
        ctk.CTkButton(hdr1, text="➕ New Booking", command=self.new_booking).pack(side="right")
        ctk.CTkButton(hdr1, text="🔄 Return Car", command=self.return_car).pack(side="right", padx=10)
        
        self.active_table = DataTable(self.tab_active, ["Trans. ID", "Customer", "Car", "Start Date", "End Date", "Total Cost"])
        
        hdr2 = ctk.CTkFrame(self.tab_all, fg_color="transparent")
        hdr2.pack(fill="x", pady=(0, 10))
        self.all_table = DataTable(self.tab_all, ["ID", "Customer", "Car", "Start Date", "End Date", "Status", "Cost", "Penalty"])
        
        self.refresh_data()
        
    def refresh_data(self):
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute('''SELECT t.id, c.name, cr.brand || ' ' || cr.model, t.start_date, t.end_date, '$' || printf('%.2f', t.total_cost)
                       FROM transactions t
                       JOIN customers c ON t.customer_id = c.id
                       JOIN cars cr ON t.car_id = cr.id
                       WHERE t.status='Active' ''')
        self.active_table.populate(cur.fetchall())
        
        cur.execute('''SELECT t.id, c.name, cr.brand || ' ' || cr.model, t.start_date, t.end_date, t.status, 
                       '$' || printf('%.2f', t.total_cost), '$' || printf('%.2f', t.penalty)
                       FROM transactions t
                       JOIN customers c ON t.customer_id = c.id
                       JOIN cars cr ON t.car_id = cr.id
                       ORDER BY t.id DESC''')
        self.all_table.populate(cur.fetchall())
        conn.close()
        
    def new_booking(self):
        win = ctk.CTkToplevel(self)
        win.title("New Booking")
        win.geometry("450x550")
        win.lift()
        win.attributes("-topmost", True)
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM customers")
        custs = [f"{r[0]} - {r[1]}" for r in cur.fetchall()]
        
        cur.execute("SELECT id, brand, model, price_per_day FROM cars WHERE status='Available'")
        cars = {f"{r[0]} - {r[1]} {r[2]}": r[3] for r in cur.fetchall()}
        conn.close()
        
        ctk.CTkLabel(win, text="Customer").pack(pady=(10,0))
        c_cb = ctk.CTkComboBox(win, values=custs)
        c_cb.pack()
        
        ctk.CTkLabel(win, text="Car").pack(pady=(10,0))
        cr_cb = ctk.CTkComboBox(win, values=list(cars.keys()))
        cr_cb.pack()
        
        ctk.CTkLabel(win, text="Start Date").pack(pady=(10,0))
        start_cal = DateEntry(win, date_pattern='y-mm-dd')
        start_cal.pack()
        
        ctk.CTkLabel(win, text="End Date").pack(pady=(10,0))
        end_cal = DateEntry(win, date_pattern='y-mm-dd')
        end_cal.pack()
        
        cost_lbl = ctk.CTkLabel(win, text="Total Cost: $0.00", font=ctk.CTkFont(weight="bold"))
        cost_lbl.pack(pady=20)
        
        def update_cost(*args):
            start = start_cal.get_date()
            end = end_cal.get_date()
            days = (end - start).days
            if days <= 0: days = 1
            selected_car = cr_cb.get()
            if selected_car in cars:
                price = cars[selected_car] * days
                cost_lbl.configure(text=f"Total Cost: ${price:.2f}")
                
        start_cal.bind("<<DateEntrySelected>>", update_cost)
        end_cal.bind("<<DateEntrySelected>>", update_cost)
        cr_cb.configure(command=update_cost)
        update_cost()
        
        def save():
            c_id = c_cb.get().split(" - ")[0]
            car_id = cr_cb.get().split(" - ")[0]
            start = start_cal.get_date()
            end = end_cal.get_date()
            days = (end - start).days
            if days <= 0: days = 1
            cost = cars[cr_cb.get()] * days
            
            conn = get_connection()
            conn.execute("INSERT INTO transactions (customer_id, car_id, start_date, end_date, total_cost, status) VALUES (?, ?, ?, ?, ?, 'Active')",
                         (c_id, car_id, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), cost))
            conn.execute("UPDATE cars SET status='Rented' WHERE id=?", (car_id,))
            conn.execute("UPDATE customers SET total_rentals=total_rentals+1 WHERE id=?", (c_id,))
            conn.commit()
            conn.close()
            self.refresh_data()
            win.destroy()
            
        ctk.CTkButton(win, text="Confirm Booking", command=save).pack(pady=10)

    def return_car(self):
        selected = self.active_table.get_selected()
        if not selected: return
        
        t_id = selected[0]
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT car_id, end_date FROM transactions WHERE id=?", (t_id,))
        car_id, end_date_str = cur.fetchone()
        
        cur.execute("SELECT value FROM settings WHERE key='late_penalty_rate'")
        res = cur.fetchone()
        penalty_rate = float(res[0]) if res else 50.0
        conn.close()
        
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        
        days_late = (today - end_date).days
        penalty = 0.0
        if days_late > 0:
            penalty = days_late * penalty_rate
            
        win = ctk.CTkToplevel(self)
        win.title("Return Car")
        win.geometry("300x300")
        win.lift()
        win.attributes("-topmost", True)
        
        ctk.CTkLabel(win, text=f"Returning Transaction {t_id}", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        ctk.CTkLabel(win, text=f"Penalty due to late return: ${penalty:.2f}").pack(pady=5)
        
        ctk.CTkLabel(win, text="Current Mileage:").pack()
        mileage_ent = ctk.CTkEntry(win)
        mileage_ent.pack(pady=5)
        
        def save():
            m = mileage_ent.get()
            if not m.isdigit(): return
            
            conn = get_connection()
            conn.execute("UPDATE transactions SET status='Completed', return_date=?, penalty=? WHERE id=?", (today.strftime('%Y-%m-%d'), penalty, t_id))
            conn.execute("UPDATE cars SET status='Available', mileage=? WHERE id=?", (m, car_id))
            conn.commit()
            conn.close()
            self.refresh_data()
            win.destroy()
            
        ctk.CTkButton(win, text="Confirm Return", command=save).pack(pady=20)
