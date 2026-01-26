import customtkinter as ctk
from tkinter import messagebox
import requests

class CurrencyConverter(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Currency Converter")
        self.geometry("450x300")
        self.configure(fg_color="#2e2f4f")

        ctk.CTkLabel(self, text="Amount:", font=("Consolas", 14)).pack(pady=(15,5))
        self.amount_entry = ctk.CTkEntry(self, font=("Consolas", 14))
        self.amount_entry.pack(pady=(0, 15), padx=30)

        ctk.CTkLabel(self, text="From Currency (e.g. USD):", font=("Consolas", 14)).pack(pady=(0,5))
        self.from_currency = ctk.CTkEntry(self, font=("Consolas", 14))
        self.from_currency.pack(pady=(0, 15), padx=30)

        ctk.CTkLabel(self, text="To Currency (e.g. INR):", font=("Consolas", 14)).pack(pady=(0,5))
        self.to_currency = ctk.CTkEntry(self, font=("Consolas", 14))
        self.to_currency.pack(pady=(0, 15), padx=30)

        convert_btn = ctk.CTkButton(self, text="Convert", command=self.convert_currency)
        convert_btn.pack(pady=10)

        self.result_label = ctk.CTkLabel(self, text="", font=("Consolas", 14))
        self.result_label.pack(pady=10)

    def convert_currency(self):
        amount = self.amount_entry.get().strip()
        from_curr = self.from_currency.get().strip().upper()
        to_curr = self.to_currency.get().strip().upper()

        if not amount or not from_curr or not to_curr:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        try:
            amount = float(amount)
        except:
            messagebox.showerror("Error", "Invalid amount!")
            return

        url = f"https://api.exchangerate.host/convert?from={from_curr}&to={to_curr}&amount={amount}"
        try:
            response = requests.get(url)
            data = response.json()
            if "result" in data:
                converted = data["result"]
                self.result_label.configure(text=f"{amount} {from_curr} = {converted:.2f} {to_curr}")
            else:
                messagebox.showerror("Error", "Failed to get conversion rate.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = CurrencyConverter()
    app.mainloop()