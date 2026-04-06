import customtkinter as ctk
from database.db_handler import get_connection
import shutil
import os
from datetime import datetime

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        header = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=28, weight="bold"))
        header.pack(anchor="w", pady=(0, 20))
        
        self.entries = {}
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT key, value FROM settings")
        for k, v in cur.fetchall():
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            ctk.CTkLabel(frame, text=k).pack(side="left", padx=10)
            e = ctk.CTkEntry(frame)
            e.insert(0, v)
            e.pack(side="right", padx=10)
            self.entries[k] = e
        conn.close()
        
        ctk.CTkButton(self, text="Save Settings", command=self.save).pack(pady=20, anchor="w")
        
        ctk.CTkLabel(self, text="Data Management", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(30, 10))
        ctk.CTkButton(self, text="Backup Database", command=self.backup_db).pack(anchor="w", pady=5)
        
        self.msg_lbl = ctk.CTkLabel(self, text="")
        self.msg_lbl.pack(anchor="w", pady=10)
        
    def save(self):
        conn = get_connection()
        for k, e in self.entries.items():
            conn.execute("UPDATE settings SET value=? WHERE key=?", (e.get(), k))
        conn.commit()
        conn.close()
        self.msg_lbl.configure(text="✅ Settings saved!", text_color="green")
        
    def backup_db(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'fleet_pro.db')
        backup_name = f"fleet_pro_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        dest_path = os.path.join(os.path.dirname(__file__), '..', backup_name)
        
        try:
            shutil.copy2(db_path, dest_path)
            self.msg_lbl.configure(text=f"✅ DB backed up: {backup_name}", text_color="green")
        except Exception as e:
            self.msg_lbl.configure(text=f"❌ Backup failed: {e}", text_color="red")
