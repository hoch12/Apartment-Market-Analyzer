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
from src.utils.config_loader import ConfigLoader

class ApartmentPriceApp:
    """
    Main GUI Application for Apartment Market Analyzer.
    
    Attributes:
        root (tk.Tk): The main window object.
        full_config (dict): Complete configuration loaded from JSON.
        app_config (dict): App-specific configuration.
        theme (dict): UI theme configuration.
        predictor (PricePredictor): Instance of the ML model wrapper.
    """
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        
        # Load Config
        try:
            self.full_config = ConfigLoader.get_config()
            self.app_config = self.full_config['app']
            self.theme = self.app_config['theme']
        except Exception as e:
            messagebox.showerror("Config Error", f"Failed to load configuration:\n{e}")
            sys.exit(1)

        self.root.title(self.app_config.get("title", "Apartment Market Analyzer"))
        self.root.geometry(self.app_config.get("window_size", "850x900"))
        self.root.resizable(True, True)

        # 1. Load Model (Mock or Real)
        self.predictor = PricePredictor()

        # 2. Define Options
        self.regions = self.predictor.get_regions()
        self.dispositions = self.predictor.get_dispositions()

        # 3. Create Design
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange all UI widgets."""
        font_family = self.app_config.get("font_family", "Segoe UI")
        bg_primary = self.theme.get("bg_primary", "#1a1a1a")
        bg_secondary = self.theme.get("bg_secondary", "#2c3e50")
        accent_color = self.theme.get("accent_color", "#e67e22")
        text_main = self.theme.get("text_main", "#ecf0f1")
        text_secondary = self.theme.get("text_secondary", "#bdc3c7")
        text_muted = self.theme.get("text_muted", "#95a5a6")
        btn_fg = self.theme.get("button_fg", "white")
        success_color = self.theme.get("success_color", "#27ae60")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=(font_family, 12), background=bg_primary, foreground=text_main)
        style.configure("TButton", font=(font_family, 12, "bold"), background=accent_color, foreground=text_main)

        self.root.configure(bg=bg_primary)

        # --- HEADER ---
        header = tk.Frame(self.root, bg=bg_secondary, pady=20)
        header.pack(fill=tk.X)
        tk.Label(header, text="Real Estate Market Analyzer", font=(font_family, 26, "bold"), bg=bg_secondary, fg=text_main).pack()
        tk.Label(header, text="Analýza cen bytů a predikce tržního vývoje", font=(font_family, 11), bg=bg_secondary,
                 fg=text_secondary).pack()

        # --- FORM ---
        form_frame = tk.Frame(self.root, bg=bg_primary, padx=40, pady=20)
        form_frame.pack(fill=tk.X)

        def add_field(label_text, variable, values=None, is_entry=False):
            container = tk.Frame(form_frame, bg=bg_primary, pady=8)
            container.pack(fill=tk.X)

            lbl = tk.Label(container, text=label_text, font=(font_family, 12), bg=bg_primary, fg=text_muted, width=20,
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

        # 1. Region
        self.region_var = tk.StringVar()
        self.region_cb = add_field("Kraj / Lokalita:", self.region_var, values=self.regions)
        if self.regions: self.region_cb.current(0)

        # 2. Disposition
        self.disp_var = tk.StringVar()
        self.disp_cb = add_field("Dispozice:", self.disp_var, values=self.dispositions)
        if self.dispositions: self.disp_cb.current(0)

        # 3. Area
        self.area_entry = add_field("Plocha (m²):", None, is_entry=True)
        self.area_entry.insert(0, "65")

        # --- BUTTON ---
        btn_frame = tk.Frame(self.root, bg=bg_primary, pady=20)
        btn_frame.pack(fill=tk.X)
        
        btn = ttk.Button(btn_frame, text="ANALYZOVAT TRŽNÍ CENU", command=self.calculate_all, style="TButton", cursor="hand2")
        btn.pack(ipady=10, ipadx=20)

        # --- RESULT ---
        self.result_label = tk.Label(self.root, text="Zadejte parametry nemovitosti",
                                     font=(font_family, 18, "bold"), bg=bg_primary, fg=success_color)
        self.result_label.pack(pady=10)

        # --- GRAPH ---
        self.graph_frame = tk.Frame(self.root, bg=bg_primary)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def validate_inputs(self, area, disp):
        """
        Check if the input area is reasonable for the given disposition.

        Args:
            area (float): Area in square meters.
            disp (str): Disposition string (e.g. "2+kk").

        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        # Approximate reasonable ranges based on data analysis
        # (min_area, max_area)
        limits = {
            "1+kk": (10, 100),
            "1+1": (20, 80),
            "2+kk": (25, 120),
            "2+1": (30, 100),
            "3+kk": (40, 180),
            "3+1": (50, 150),
            "4+kk": (60, 300),
            "4+1": (70, 200),
            "5+kk": (90, 400),
            "5+1": (90, 300),
            "6+kk": (140, 600)
        }
        
        if disp in limits:
            min_a, max_a = limits[disp]
            if area < min_a:
                return False, f"Plocha {area} m² je pro dispozici {disp} podezřele malá.\nObvyklé minimum je cca {min_a} m²."
            if area > max_a:
                return False, f"Plocha {area} m² je pro dispozici {disp} podezřele velká.\nObvyklé maximum je cca {max_a} m²."
        
        return True, ""

    def calculate_all(self):
        """
        Trigger the prediction process and update the UI with results.
        Called when the analysis button is clicked.
        """
        try:
            current_price = self.get_prediction()
            if current_price is None: return

            formatted = f"{int(current_price):,}".replace(",", " ")
            self.result_label.config(text=f"Odhadovaná cena: {formatted} Kč")

            self.plot_future_trend(current_price)

        except Exception as e:
            messagebox.showerror("Chyba", str(e))

    def get_prediction(self):
        """
        Gather inputs, validate them, and perform inference using the model.

        Returns:
            float: Predicted price in CZK, or None if validation fails.
        """
        try:
            area = float(self.area_entry.get())
        except ValueError:
            messagebox.showwarning("Chyba", "Plocha musí být číslo!")
            return None

        if area <= 0 or area > 1000:
            messagebox.showwarning("Chyba", "Zadejte reálnou plochu bytu.")
            return None

        # Logic Validation (Area vs Disposition)
        disp = self.disp_var.get()
        valid, msg = self.validate_inputs(area, disp)
        if not valid:
             # Ask user if they want to proceed despite the warning
            response = messagebox.askyesno("Varování - Neobvyklá hodnota", 
                                           f"{msg}\n\nChcete přesto pokračovat?")
            if not response:
                return None

        region = self.region_var.get()

        try:
            return self.predictor.predict_price(area, disp, region)
        except Exception as e:
            # For demonstration if model is not trained yet:
            # return area * 100000 
            messagebox.showerror("Model Error", f"Model není připraven na tato data nebo nebyl nalezen.\n{e}")
            return None

    def plot_future_trend(self, start_price):
        """
        Visualize the future value of the property using matplotlib.

        Args:
            start_price (float): The current predicted price.
        """
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        bg_primary = self.theme.get("bg_primary", "#1a1a1a")
        text_main = self.theme.get("text_main", "#ecf0f1")
        accent_color = self.theme.get("accent_color", "#e67e22")
        success_color = self.theme.get("success_color", "#27ae60")

        future_data = self.predictor.calculate_future_value(start_price, years=10, growth_rate=0.04) 
        years = [d['year'] for d in future_data]
        prices = [d['price'] for d in future_data]

        fig = Figure(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor(bg_primary)
        ax = fig.add_subplot(111)
        ax.set_facecolor(bg_primary)

        ax.plot(years, prices, marker='s', linestyle='-', color=accent_color, linewidth=2, markersize=6)

        for spine in ax.spines.values():
            spine.set_color(text_main)

        ax.tick_params(colors=text_main)
        ax.set_title("Očekávaný vývoj hodnoty nemovitosti (10 let)", fontsize=12, color=text_main)
        ax.set_ylabel("Hodnota (Kč)", color=text_main)
        ax.grid(True, linestyle='--', alpha=0.2, color=text_main)

        def currency_formatter(x, pos):
            if x >= 1_000_000:
                return f'{x*1e-6:.1f}M'
            else:
                return f'{x*1e-3:.0f}k'

        ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ApartmentPriceApp(root)
    root.mainloop()