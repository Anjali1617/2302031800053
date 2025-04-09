import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox
import json
import os
from datetime import datetime

class CurrencyConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Currency Converter")
        self.geometry("600x400")
        self.minsize(400, 300)
        
        # Configure grid expansion
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configure main frame grid expansion
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        for i in range(7):
            self.main_frame.grid_rowconfigure(i, weight=1)
        
        # Load currencies
        self.currencies = self.load_currencies()
        self.exchange_rates = self.load_exchange_rates()
        
        # Create widgets
        self.create_widgets()
        
    def load_currencies(self):
        """Load list of currencies from file or API"""
        try:
            # Try to load from local file first
            if os.path.exists("currencies.json"):
                with open("currencies.json", "r") as file:
                    return json.load(file)
            
            # If file doesn't exist, fetch from API
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            data = response.json()
            currencies = {"USD": "US Dollar"}
            
            # For demo purposes, adding some common currencies
            currencies = {
                "USD": "US Dollar",
                "EUR": "Euro",
                "GBP": "British Pound",
                "JPY": "Japanese Yen",
                "CAD": "Canadian Dollar",
                "AUD": "Australian Dollar",
                "INR": "Indian Rupee",
                "CNY": "Chinese Yuan",
                "RUB": "Russian Ruble",
                "MXN": "Mexican Peso"
            }
            
            # Save to file for future use
            with open("currencies.json", "w") as file:
                json.dump(currencies, file)
                
            return currencies
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load currencies: {str(e)}")
            return {"USD": "US Dollar", "EUR": "Euro", "GBP": "British Pound"}
    
    def load_exchange_rates(self):
        """Load exchange rates from API or cached file"""
        try:
            # Check if we have a recent cache (less than 1 day old)
            if os.path.exists("exchange_rates.json"):
                with open("exchange_rates.json", "r") as file:
                    data = json.load(file)
                    # Check if the data is still valid (less than 24 hours old)
                    if datetime.now().timestamp() - data["timestamp"] < 86400:  # 24 hours in seconds
                        return data["rates"]
            
            # Fetch new data
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            data = response.json()
            
            # Cache the data
            cache_data = {
                "timestamp": datetime.now().timestamp(),
                "rates": data["rates"]
            }
            with open("exchange_rates.json", "w") as file:
                json.dump(cache_data, file)
                
            return data["rates"]
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load exchange rates: {str(e)}")
            # Return some sample rates for demonstration
            return {
                "USD": 1,
                "EUR": 0.85,
                "GBP": 0.75,
                "JPY": 110.25,
                "CAD": 1.25,
                "AUD": 1.35,
                "INR": 74.5,
                "CNY": 6.5,
                "RUB": 75.8,
                "MXN": 20.3
            }
    
    def create_widgets(self):
        """Create all the UI elements"""
        # Title
        title_label = ttk.Label(self.main_frame, text="Currency Converter", font=("Helvetica", 20))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="n")
        
        # Amount input
        amount_label = ttk.Label(self.main_frame, text="Amount:", font=("Helvetica", 14))
        amount_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.amount_entry = ttk.Entry(self.main_frame, font=("Helvetica", 12))
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.amount_entry.insert(0, "1")
        
        # From currency dropdown
        from_label = ttk.Label(self.main_frame, text="From Currency:", font=("Helvetica", 14))
        from_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.from_currency = tk.StringVar()
        self.from_currency.set("USD")
        
        # Create a list of currency options with their names
        currency_options = [f"{code} - {name}" for code, name in self.currencies.items()]
        
        from_dropdown = ttk.Combobox(self.main_frame, textvariable=self.from_currency, values=currency_options, font=("Helvetica", 12))
        from_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        from_dropdown.current(0)
        
        # To currency dropdown
        to_label = ttk.Label(self.main_frame, text="To Currency:", font=("Helvetica", 14))
        to_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        self.to_currency = tk.StringVar()
        self.to_currency.set("EUR")
        
        to_dropdown = ttk.Combobox(self.main_frame, textvariable=self.to_currency, values=currency_options, font=("Helvetica", 12))
        to_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        to_dropdown.current(1)
        
        # Convert button
        convert_button = ttk.Button(self.main_frame, text="Convert", command=self.convert_currency, style="Accent.TButton")
        convert_button.grid(row=4, column=0, columnspan=2, pady=20, sticky="n")
        
        # Create a style for the button
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Helvetica", 14), padding=10)
        
        # Result display
        result_frame = ttk.LabelFrame(self.main_frame, text="Conversion Result", padding=10)
        result_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        result_frame.grid_columnconfigure(0, weight=1)
        
        self.result_label = ttk.Label(result_frame, text="", font=("Helvetica", 16))
        self.result_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Status bar
        self.status_bar = ttk.Label(self.main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=6, column=0, columnspan=2, sticky="ew")
    
    def convert_currency(self):
        """Handle the currency conversion"""
        try:
            # Get input values
            amount = float(self.amount_entry.get())
            from_currency_full = self.from_currency.get()
            to_currency_full = self.to_currency.get()
            
            # Extract currency codes from the dropdown values
            from_code = from_currency_full.split(' - ')[0]
            to_code = to_currency_full.split(' - ')[0]
            
            # Check if we need to update exchange rates
            self.exchange_rates = self.load_exchange_rates()
            
            # Perform conversion
            if from_code == "USD":
                # Direct conversion from USD
                rate = self.exchange_rates.get(to_code, 1.0)
                result = amount * rate
            elif to_code == "USD":
                # Direct conversion to USD
                rate = self.exchange_rates.get(from_code, 1.0)
                result = amount / rate
            else:
                # Convert via USD
                from_rate = self.exchange_rates.get(from_code, 1.0)
                to_rate = self.exchange_rates.get(to_code, 1.0)
                result = amount / from_rate * to_rate
            
            # Display result
            self.result_label.config(text=f"{amount:.2f} {from_code} = {result:.2f} {to_code}")
            self.status_bar.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
            
if __name__ == "__main__":
    app = CurrencyConverter()
    # Apply theme
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme
    app.mainloop()
