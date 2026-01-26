import customtkinter as ctk
from tkinter import simpledialog, messagebox
import os
import shutil

class FileExplorer(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("📁 File Explorer")
        self.geometry("850x500")
        self.configure(fg_color="#2e2f4f")

        # Main Frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Sidebar
        self.sidebar = ctk.CTkFrame(main_frame, width=200, fg_color="#1f1f33", corner_radius=15)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))

        # Right Content Area
        self.listbox = ctk.CTkTextbox(main_frame, corner_radius=15, fg_color="#1f1f33", text_color="white")
        self.listbox.pack(side="right", fill="both", expand=True)


        self.create_sidebar_buttons()
        self.load_items()

    def create_sidebar_buttons(self):
        # Only these 4 folders
        special_folders = {
            "📂 3D Objects": os.path.join(os.path.expanduser("~"), "3D Objects"),
            "🖥 Desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
            "📄 Documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "⬇️ Downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
            "🎵 Music": os.path.join(os.path.expanduser("~"), "Music"),
            "🖼 Pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
            "📹 Videos": os.path.join(os.path.expanduser("~"), "Videos")
        }

        for name, path in special_folders.items():
            ctk.CTkButton(self.sidebar, text=name, command=lambda p=path: self.change_path(p),
                          fg_color="#5e5ad6", hover_color="#7a78f5", corner_radius=20, height=30).pack(pady=6, fill="x", padx=10)

    def change_path(self, path):
        self.current_path = path
        self.load_items()

    def load_items(self):
        self.listbox.delete("0.0", "end")
        try:
            items = os.listdir(self.current_path)
            items.sort()
            for item in items:
                self.listbox.insert("end", f"{item}\n")
        except Exception as e:
            self.listbox.insert("end", f"[Error] {e}")

if __name__ == "__main__":
    app = FileExplorer()
    app.mainloop()