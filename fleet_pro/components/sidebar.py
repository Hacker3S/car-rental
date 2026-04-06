import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, navigate_callback, toggle_theme_callback):
        super().__init__(master, width=250, corner_radius=0)
        
        self.navigate_callback = navigate_callback
        self.toggle_theme_callback = toggle_theme_callback
        
        # Logo
        self.logo_label = ctk.CTkLabel(self, text="🚗 FleetPro", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Nav Buttons
        self.nav_buttons = {}
        pages = ["Dashboard", "Fleet", "Customers", "Suppliers", "Bookings", "Reports", "Settings"]
        
        for i, page in enumerate(pages, start=1):
            btn = ctk.CTkButton(self, text=page, fg_color="transparent", text_color=("gray10", "gray90"),
                                hover_color=("gray70", "gray30"), anchor="w",
                                command=lambda p=page: self.select_page(p))
            btn.grid(row=i, column=0, pady=5, padx=20, sticky="ew")
            self.nav_buttons[page] = btn
            
        # Bottom controls
        self.grid_rowconfigure(len(pages)+1, weight=1)
        self.theme_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self._toggle_theme)
        self.theme_switch.grid(row=len(pages)+2, column=0, padx=20, pady=20, sticky="s")
        self.theme_switch.select() # Default Dark
        
    def _toggle_theme(self):
        is_dark = self.theme_switch.get() == 1
        self.toggle_theme_callback("Dark" if is_dark else "Light")
        
    def select_page(self, page_name):
        # Update styling
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")
        # Call router
        self.navigate_callback(page_name)
