import customtkinter as ctk
from app import App
from database.db_handler import initialize_db

if __name__ == "__main__":
    initialize_db()
    
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    app = App()
    app.mainloop()
