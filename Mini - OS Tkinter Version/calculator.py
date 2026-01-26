import customtkinter as ctk

class Calculator(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Calculator")
        self.geometry("320x450")
        self.configure(fg_color="#2e2f4f")
        
        self.expression = ""
        
        # Display
        self.display = ctk.CTkEntry(self, font=("Consolas", 24), justify="right", corner_radius=10)
        self.display.pack(fill="x", padx=10, pady=15)
        self.display.configure(state="readonly")
        
        # Buttons Frame
        btns_frame = ctk.CTkFrame(self, fg_color="#1f1f33", corner_radius=15)
        btns_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "C", "+"],
            ["="]
        ]
        
        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                btn = ctk.CTkButton(
                    btns_frame, text=char, width=60, height=50,
                    fg_color="#5e5ad6", hover_color="#7a78f5", corner_radius=20,
                    command=lambda ch=char: self.on_button_click(ch)
                )
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
        
        # Make buttons expand evenly
        for i in range(4):
            btns_frame.grid_columnconfigure(i, weight=1)
        for i in range(len(buttons)):
            btns_frame.grid_rowconfigure(i, weight=1)
        
    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
            self.update_display()
        elif char == "=":
            try:
                result = str(eval(self.expression))
                self.expression = result
                self.update_display()
            except Exception:
                self.expression = ""
                self.update_display("Error")
        else:
            self.expression += char
            self.update_display()
            
    def update_display(self, text=None):
        if text is None:
            text = self.expression
        self.display.configure(state="normal")
        self.display.delete(0, "end")
        self.display.insert(0, text)
        self.display.configure(state="readonly")

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()