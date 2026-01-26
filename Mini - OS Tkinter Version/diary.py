import customtkinter as ctk
from tkinter import messagebox
import os

class Diary(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Diary")
        self.geometry("600x500")
        self.configure(fg_color="#2e2f4f")
        
        # Folder jahan diary files save hongi
        self.diary_folder = os.path.join(os.path.expanduser("~"), "MiniOS_Diary")
        if not os.path.exists(self.diary_folder):
            os.makedirs(self.diary_folder)
        
        # Entry title (date or custom)
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Entry Title (e.g. 2025-06-08)", font=("Consolas", 16))
        self.title_entry.pack(fill="x", padx=15, pady=(15,5))
        
        # Text box
        self.text_box = ctk.CTkTextbox(self, font=("Consolas", 14), wrap="word")
        self.text_box.pack(expand=True, fill="both", padx=15, pady=10)
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(self, fg_color="#1f1f33")
        btn_frame.pack(fill="x", padx=15, pady=(0,15))
        
        save_btn = ctk.CTkButton(btn_frame, text="Save Entry", command=self.save_entry, fg_color="#5e5ad6", hover_color="#7a78f5")
        save_btn.pack(side="left", padx=10, pady=10)
        
        load_btn = ctk.CTkButton(btn_frame, text="Load Entry", command=self.load_entry, fg_color="#5e5ad6", hover_color="#7a78f5")
        load_btn.pack(side="left", padx=10, pady=10)
        
        clear_btn = ctk.CTkButton(btn_frame, text="Clear", command=self.clear_text, fg_color="#5e5ad6", hover_color="#7a78f5")
        clear_btn.pack(side="right", padx=10, pady=10)
    
    def save_entry(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Please enter a title for your diary entry.")
            return
        
        filename = f"{title}.txt"
        path = os.path.join(self.diary_folder, filename)
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                content = self.text_box.get("1.0", "end-1c")
                f.write(content)
            messagebox.showinfo("Success", f"Entry '{title}' saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save entry.\n{str(e)}")
    
    def load_entry(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Please enter the title of the entry to load.")
            return
        
        filename = f"{title}.txt"
        path = os.path.join(self.diary_folder, filename)
        
        if not os.path.exists(path):
            messagebox.showerror("Error", f"No entry found with the title '{title}'.")
            return
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_box.delete("1.0", "end")
            self.text_box.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load entry.\n{str(e)}")
    
    def clear_text(self):
        self.text_box.delete("1.0", "end")
        self.title_entry.delete(0, "end")

if __name__ == "__main__":
    app = Diary()
    app.mainloop()