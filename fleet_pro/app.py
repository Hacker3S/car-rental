import customtkinter as ctk
from components.sidebar import Sidebar

from pages.dashboard import DashboardPage
from pages.fleet import FleetPage
from pages.customers import CustomersPage
from pages.suppliers import SuppliersPage
from pages.bookings import BookingsPage
from pages.reports import ReportsPage
from pages.settings import SettingsPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FleetPro - Car Rental Management SaaS")
        self.geometry("1400x850")
        
        try:
            self.state("zoomed")
        except Exception:
            self.attributes('-zoomed', True)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.sidebar_frame = Sidebar(self, self.navigate, self.toggle_theme)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        self.pages = {
            "Dashboard": DashboardPage,
            "Fleet": FleetPage,
            "Customers": CustomersPage,
            "Suppliers": SuppliersPage,
            "Bookings": BookingsPage,
            "Reports": ReportsPage,
            "Settings": SettingsPage
        }
        
        self.current_frame = None
        self.sidebar_frame.select_page("Dashboard")
        
    def navigate(self, page_name):
        if self.current_frame is not None:
            self.current_frame.destroy()
            
        page_class = self.pages.get(page_name)
        if page_class:
            self.current_frame = page_class(self.content_frame)
            self.current_frame.grid(row=0, column=0, sticky="nsew")
        else:
            self.current_frame = ctk.CTkFrame(self.content_frame)
            self.current_frame.grid(row=0, column=0, sticky="nsew")
            ctk.CTkLabel(self.current_frame, text=f"{page_name} under construction").pack(expand=True)
            
    def toggle_theme(self, mode):
        ctk.set_appearance_mode(mode)
