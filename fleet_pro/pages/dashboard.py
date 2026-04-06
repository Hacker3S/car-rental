import customtkinter as ctk
from database.db_handler import get_connection
from components.kpi_card import KPICard
from components.data_table import DataTable
from utils.chart_builder import create_bar_chart, create_pie_chart

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        header = ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size=28, weight="bold"))
        header.pack(anchor="w", pady=(0, 20))
        
        self.alert_banner = ctk.CTkLabel(self, text="⚠️ Low Fleet Alert: Available cars below threshold!", 
                                       text_color="white", fg_color="#E74C3C", corner_radius=5, font=ctk.CTkFont(weight="bold"))
        
        self.kpi_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.kpi_frame.pack(fill="x", pady=(0, 20))
        
        self.kpis = {}
        for col, title in enumerate(["Total Cars", "Available", "Active Rentals", "Total Revenue"]):
            self.kpi_frame.columnconfigure(col, weight=1)
            card = KPICard(self.kpi_frame, title, "0")
            card.grid(row=0, column=col, sticky="ew", padx=5)
            self.kpis[title] = card
            
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)
        
        self.chart_left_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.chart_left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.chart_right_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.chart_right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        self.transactions_frame = ctk.CTkFrame(self, corner_radius=10)
        self.transactions_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(self.transactions_frame, text="Recent Transactions", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=20, pady=10)
        self.table = DataTable(self.transactions_frame, ["ID", "Customer", "Car", "Status", "Amount"])
        
        self.fig_left = None
        self.fig_right = None
        
        self.refresh_data()
        
    def refresh_data(self):
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM cars")
        total_cars = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM cars WHERE status='Available'")
        available = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM transactions WHERE status='Active'")
        active = cur.fetchone()[0]
        
        cur.execute("SELECT SUM(total_cost) FROM transactions")
        rev = cur.fetchone()[0]
        total_rev = f"${rev:.2f}" if rev else "$0.00"
        
        self.kpis["Total Cars"].update_value(total_cars)
        self.kpis["Available"].update_value(available)
        self.kpis["Active Rentals"].update_value(active)
        self.kpis["Total Revenue"].update_value(total_rev)
        
        cur.execute("SELECT value FROM settings WHERE key='low_fleet_threshold'")
        res = cur.fetchone()
        threshold = int(res[0]) if res else 2
        
        if available < threshold:
            self.alert_banner.pack(fill="x", pady=(0, 20), before=self.kpi_frame)
        else:
            self.alert_banner.pack_forget()
            
        cur.execute('''SELECT t.id, c.name, cr.brand || ' ' || cr.model, t.status, '$' || printf('%.2f', t.total_cost) 
                       FROM transactions t
                       JOIN customers c ON t.customer_id = c.id
                       JOIN cars cr ON t.car_id = cr.id
                       ORDER BY t.id DESC LIMIT 5''')
        self.table.populate(cur.fetchall())
        
        if self.fig_left: self.fig_left.destroy()
        if self.fig_right: self.fig_right.destroy()
        
        # Monthly Revenue
        cur.execute("SELECT start_date, total_cost FROM transactions")
        rows = cur.fetchall()
        months = {str(i).zfill(2): 0 for i in range(1, 13)}
        
        for r in rows:
            try:
                m = r[0].split('-')[1]
                months[m] += r[1]
            except: pass
            
        m_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        m_vals = [months[str(i).zfill(2)] for i in range(1, 13)]
        
        self.fig_left = create_bar_chart(self.chart_left_frame, m_names, m_vals, "Monthly Revenue", "Month", "Revenue")
        self.fig_left.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Fleet Status
        cur.execute("SELECT status, COUNT(*) FROM cars GROUP BY status")
        s_data = cur.fetchall()
        labels = [s[0] for s in s_data]
        sizes = [s[1] for s in s_data]
        
        if sum(sizes) > 0:
            self.fig_right = create_pie_chart(self.chart_right_frame, labels, sizes, "Fleet Status")
            self.fig_right.pack(fill="both", expand=True, padx=10, pady=10)
            
        conn.close()
