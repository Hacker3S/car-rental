import customtkinter as ctk
from tkinter import ttk

class DataTable(ctk.CTkFrame):
    def __init__(self, master, columns, show_id=True, allow_selection=True):
        super().__init__(master, corner_radius=10)
        
        style = ttk.Style()
        style.theme_use("default")
        bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        bg = bg_color[1] if ctk.get_appearance_mode() == "Dark" else bg_color[0]
        
        style.configure("Treeview", 
                        background=bg,
                        foreground="white" if ctk.get_appearance_mode()=="Dark" else "black",
                        rowheight=35,
                        fieldbackground=bg,
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#1F6FEB')], foreground=[('selected', 'white')])
        
        style.configure("Treeview.Heading",
                        background="#2C2C2C" if ctk.get_appearance_mode()=="Dark" else "#E5E5E5",
                        foreground="white" if ctk.get_appearance_mode()=="Dark" else "black",
                        relief="flat",
                        font=('Arial', 10, 'bold'))
        
        self.tree = ttk.Treeview(self, columns=columns, show="headings" if show_id else "tree")
        if show_id:
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor="center")
                
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10)
        
    def populate(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)
            
    def get_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])['values']
        return None
        
    def bind_double_click(self, callback):
        self.tree.bind("<Double-1>", callback)
