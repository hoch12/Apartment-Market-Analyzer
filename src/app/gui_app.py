import tkinter as tk
from tkinter import ttk, messagebox
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
import datetime
import os

# Add project root to path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from src.model.inference import PricePredictor

# --- KONFIGURACE ---
DEPRECIATION_RATE = 0.10  # 10 % ročně
CURRENT_YEAR = datetime.datetime.now().year


class CarPriceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced AI Car Price Estimator")
        # Increased window size to fit comfortably on Mac
        self.root.geometry("800x950")
        self.root.resizable(True, True)  # Allow resizing just in case

        # 1. Load Model
        try:
            self.predictor = PricePredictor()
            print("✅ Model and columns loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model!\n{e}")
            sys.exit()

        # 2. Define Options
        self.fuel_types = ['Petrol', 'Diesel', 'Electric', 'LPG', 'Hybrid', 'CNG']
        self.transmissions = ['Manual', 'Automatic']
        self.brands = self.predictor.get_clean_brands()

        # 3. Create Design
        self.create_widgets()

    # get_project_root, load_model_data, get_clean_brands removed as they are now in PricePredictor


    def create_widgets(self):
        # --- STYLES ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=("Segoe UI", 12), background="#2b2b2b", foreground="white")
        style.configure("TButton", font=("Segoe UI", 12, "bold"), background="#007acc", foreground="white")

        self.root.configure(bg="#2b2b2b")

        # --- HEADER ---
        header = tk.Frame(self.root, bg="#1e1e1e", pady=20)
        header.pack(fill=tk.X)
        tk.Label(header, text="AI Car Market Analyzer", font=("Segoe UI", 26, "bold"), bg="#1e1e1e", fg="white").pack()
        tk.Label(header, text="Market Price Prediction & Future Trends", font=("Segoe UI", 11), bg="#1e1e1e",
                 fg="#aaaaaa").pack()

        # --- FORM (Using PACK for stability on Mac) ---
        form_frame = tk.Frame(self.root, bg="#2b2b2b", padx=40, pady=20)
        form_frame.pack(fill=tk.X)

        def add_field(label_text, variable, values=None, is_entry=False):
            container = tk.Frame(form_frame, bg="#2b2b2b", pady=5)
            container.pack(fill=tk.X)

            lbl = tk.Label(container, text=label_text, font=("Segoe UI", 12), bg="#2b2b2b", fg="#dddddd", width=20,
                           anchor="w")
            lbl.pack(side=tk.LEFT)

            if is_entry:
                widget = ttk.Entry(container, width=30)
                widget.pack(side=tk.LEFT, padx=10)
                return widget
            else:
                widget = ttk.Combobox(container, textvariable=variable, values=values, state="readonly", width=28)
                widget.pack(side=tk.LEFT, padx=10)
                return widget

        # 1. Brand
        self.brand_var = tk.StringVar()
        self.brand_cb = add_field("Car Brand:", self.brand_var, values=self.brands)
        if self.brands: self.brand_cb.current(0)

        # 2. Year
        self.year_entry = add_field("Year of Manufacture:", None, is_entry=True)
        self.year_entry.insert(0, str(datetime.datetime.now().year - 4))

        # 3. Mileage
        self.mileage_entry = add_field("Mileage (km):", None, is_entry=True)
        self.mileage_entry.insert(0, "65000")

        # 4. Fuel
        self.fuel_var = tk.StringVar()
        self.fuel_cb = add_field("Fuel Type:", self.fuel_var, values=self.fuel_types)
        self.fuel_cb.current(0)

        # 5. Transmission
        self.trans_var = tk.StringVar()
        self.trans_cb = add_field("Transmission:", self.trans_var, values=self.transmissions)
        self.trans_cb.current(0)

        # --- BUTTON ---
        btn_frame = tk.Frame(self.root, bg="#2b2b2b", pady=20)
        btn_frame.pack(fill=tk.X)
        # Changed button text color to black (fg="black") as requested
        btn = tk.Button(btn_frame, text="CALCULATE PRICE & PREDICTION", command=self.calculate_all,
                        bg="#007acc", fg="black", font=("Segoe UI", 13, "bold"), padx=30, pady=12, relief="flat")
        btn.pack()

        # --- RESULT ---
        self.result_label = tk.Label(self.root, text="Enter data and click the button",
                                     font=("Segoe UI", 18, "bold"), bg="#2b2b2b", fg="#4CAF50")
        self.result_label.pack(pady=10)

        # --- GRAPH ---
        self.graph_frame = tk.Frame(self.root, bg="#2b2b2b")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def calculate_all(self):
        try:
            current_price = self.predict_current_price()
            if current_price is None: return

            formatted = f"{int(current_price):,}".replace(",", " ")
            self.result_label.config(text=f"Current Estimate: {formatted} CZK")

            self.plot_future_trend(current_price)

        except Exception as e:
            messagebox.showerror("Critical Error", str(e))

    def predict_current_price(self):
        # --- VALIDATION ---
        try:
            year = int(self.year_entry.get())
            mileage = int(self.mileage_entry.get())
        except ValueError:
            messagebox.showwarning("Error", "Year and mileage must be numbers!")
            return None

        current_year = datetime.datetime.now().year
        if year < 1980 or year > current_year + 1:
            messagebox.showwarning("Error", f"Year must be between 1980 and {current_year + 1}.")
            return None

        if mileage < 0 or mileage > 2000000:
            messagebox.showwarning("Error", "Mileage is out of realistic range.")
            return None

        brand = self.brand_var.get()
        fuel = self.fuel_var.get()
        trans = self.trans_var.get()

        if not brand:
            messagebox.showwarning("Error", "Select a brand!")
            return None

        # --- USE PREDICTOR ---
        try:
            price = self.predictor.predict_price(year, mileage, brand, fuel, trans)
            return price
        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))
            return None

    def plot_future_trend(self, start_price):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        future_data = self.predictor.calculate_future_value(start_price, years=5, depreciation_rate=DEPRECIATION_RATE)
        years = [d['year'] for d in future_data]
        prices = [d['price'] for d in future_data]

        # Použití Figure objektu místo pyplot (předejití memory leak)
        fig = Figure(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#2b2b2b')

        ax.plot(years, prices, marker='o', linestyle='-', color='#007acc', linewidth=3, markersize=8)

        # Barvy grafu (aby byly vidět na tmavém pozadí)
        for spine in ax.spines.values():
            spine.set_color('white')

        ax.tick_params(colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.set_title(f"Price Trend Prediction ({years[0]}-{years[-1]})", fontsize=12, color='white')
        ax.set_ylabel("Price (CZK)", color='white')
        ax.grid(True, linestyle='--', alpha=0.3, color='white')

        # Format Y-axis to avoid scientific notation and use 'k' or 'M'
        def currency_formatter(x, pos):
            if x >= 1_000_000:
                return f'{x*1e-6:.1f}M'
            else:
                return f'{x*1e-3:.0f}k'

        ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))

        # Popisky
        for i, price in enumerate(prices):
            formatted_k = f"{int(price / 1000)}k"
            ax.annotate(formatted_k, (years[i], prices[i]), textcoords="offset points", xytext=(0, 10), ha='center',
                        color="#4CAF50", fontweight='bold')

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = CarPriceApp(root)
    root.mainloop()