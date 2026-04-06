import customtkinter as ctk

class ModalForm(ctk.CTkToplevel):
    def __init__(self, master, title, fields, on_submit):
        super().__init__(master)
        self.title(title)
        self.geometry("400x500")
        
        # Bring to front and grab focus
        self.lift()
        self.attributes("-topmost", True)
        self.after(10, self._grab_focus)
        
        self.on_submit = on_submit
        self.inputs = {}
        self.fields_config = fields
        
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(self.scroll_frame, text=title, font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        
        for field in fields:
            label = field.get("label")
            ftype = field.get("type", "entry")
            
            ctk.CTkLabel(self.scroll_frame, text=label).pack(anchor="w", pady=(10, 0))
            
            if ftype == "entry":
                inp = ctk.CTkEntry(self.scroll_frame)
                inp.pack(fill="x")
                if "default" in field:
                    inp.insert(0, str(field["default"]))
                self.inputs[label] = inp
                
            elif ftype == "dropdown":
                inp = ctk.CTkComboBox(self.scroll_frame, values=field.get("options", []))
                inp.pack(fill="x")
                if "default" in field:
                    inp.set(field["default"])
                self.inputs[label] = inp
                
        # Error Label
        self.error_label = ctk.CTkLabel(self.scroll_frame, text="", text_color="red")
        self.error_label.pack(pady=5)
                
        btn_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="gray", command=self.destroy).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(btn_frame, text="Save", command=self._submit).pack(side="right", expand=True, padx=5)
        
    def _grab_focus(self):
        self.grab_set()
        self.focus_force()

    def _submit(self):
        data = {k: v.get() for k, v in self.inputs.items()}
        
        # Validations if any
        for field in self.fields_config:
            if field.get("required", False) and not data[field["label"]]:
                self.error_label.configure(text=f"{field['label']} is required")
                return
            if field.get("numeric", False) and not data[field["label"]].replace('.', '', 1).isdigit():
                self.error_label.configure(text=f"{field['label']} must be numeric")
                return
                
        if self.on_submit(data):
            self.destroy()
        else:
            self.error_label.configure(text="Submission failed.")
