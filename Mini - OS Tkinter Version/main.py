import customtkinter as ctk
from auth import AuthWindow
import subprocess
import os

class MiniOS(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mini OS - Dashboard")
        self.geometry("800x500")
        self.configure(fg_color="#1e1b3a")
        self.resizable(False, False)

        # Only apps that actually exist should be listed
        self.app_buttons = {
            "🧮 Calculator ": "calculator.py",
            "📒 Diary ": "diary.py",
            "📜 Notes ": "notes.py",
            "💱 Currency Converter ": "currency_converter.py",
            "📂 File Explorer ": "file_explorer.py",
            "🔐 Security": "security.py"
            # Add back "Password Manager" and others when their files are ready
        }

        self.init_ui()

    def init_ui(self):
        ctk.CTkLabel(self, text="Welcome to Mini OS", font=("Helvetica", 24, "bold"), text_color="#ffffff").pack(pady=30)

        btn_frame = ctk.CTkFrame(self, fg_color="#29264b", corner_radius=15)
        btn_frame.pack(pady=20)

        for app_name, app_file in self.app_buttons.items():
            btn = ctk.CTkButton(btn_frame, text=app_name, width=200, height=45, corner_radius=30,
                                fg_color="#6a5acd", hover_color="#7c70ee", font=("Helvetica", 14, "bold"),
                                command=lambda f=app_file: self.launch_app(f))
            btn.pack(pady=10)

    def launch_app(self, file_name):
        try:
            # Ensure the file exists before trying to launch
            if not os.path.isfile(file_name):
                print(f"App file {file_name} does not exist.")
                return
            # Launch the app using subprocess
            # Using "python" to ensure it runs in the same environment
            if not file_name.endswith('.py'):
                print(f"Invalid app file: {file_name}")
                return
            # Debugging output
            print("Launching app:", file_name)  # Debug
            subprocess.Popen(["python", file_name])
            print("App launched successfully:", file_name)
            
        except Exception as e:
            print("Error launching app:", e)

# This function will be called after successful login
def launch_os():
    app = MiniOS()
    app.mainloop()

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()

    def open_main_os():
        root.quit()
        launch_os()

    # AuthWindow will handle login/signup and then call launch_os
    auth = AuthWindow(None, login_success_callback=open_main_os)
    auth.mainloop()
