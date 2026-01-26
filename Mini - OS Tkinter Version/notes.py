import customtkinter as ctk

class Notes(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Notes")
        self.geometry("600x450")
        self.configure(fg_color="#2e2f4f")
        
        self.text_box = ctk.CTkTextbox(self, font=("Consolas", 14), wrap="word")
        self.text_box.pack(expand=True, fill="both", padx=15, pady=15)
        
        clear_btn = ctk.CTkButton(self, text="Clear Notes", command=self.clear_notes, fg_color="#5e5ad6", hover_color="#7a78f5")
        clear_btn.pack(pady=(0,15))
    
    def clear_notes(self):
        self.text_box.delete("1.0", "end")

if __name__ == "__main__":
    app = Notes()
    app.mainloop()