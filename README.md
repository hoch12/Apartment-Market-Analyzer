# Apartment Market Analyzer

Apartment Market Analyzer is a machine learning-powered desktop application that estimates the market price of apartments in the Czech Republic and predicts their future value trends (10-year projection).

## 📌 Features
- **Market Price Estimation**: Price prediction based on location (region), layout (1+kk to 5+1), and usable area.
- **Future Value Projection**: Visualization of expected property value growth over a ten-year horizon.
- **Data-Driven**: The application uses data scraped directly from real estate portals.
- **Modern GUI**: User-friendly interface built with Tkinter.

---

## 📂 Project Structure

```
Apartment-Market-Analyzer/
├── data/                  # Data storage
│   └── raw/               # Raw scraped data
├── docs/                  # Detailed documentation
├── src/
│   ├── app/
│   │   └── gui_app.py     # Main GUI entry point
│   ├── model/
│   │   ├── inference.py   # Prediction logic and internal API
│   │   ├── train_model.py # Model training script
│   │   └── *.pkl          # Trained model artifacts
│   └── scraper/
│       └── reality_scraper.py # Real estate web scraper
├── requirements.txt       # Project dependencies
└── README.md              # Main documentation
```

---

## 🛠️ Technologies

- **`scikit-learn`**: Random Forest Regressor for price prediction.
- **`pandas`**: Data manipulation and cleaning.
- **`matplotlib`**: Price trend visualization.
- **`selenium`**: Scraping dynamic content from real estate websites.
- **`tkinter`**: Application interface.

---

## 🚀 How to Run

### 0. Prerequisites
Ensure you have Python 3.9+ installed and Google Chrome (for scraping).

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Data Collection (Optional)
If you want to scrape fresh data from real estate portals:
```bash
python src/scraper/reality_scraper.py
```
*Note: This will open a browser window. You must manually accept cookies and then press ENTER in the terminal.*

### 3. Model Training
After collecting data, you need to train the model to improve accuracy or use new data:
```bash
python src/model/train_model.py
```
*This will generate `.pkl` files in `src/model/` used by the application.*

### 4. Run the Application
Start the GUI application:
```bash
python src/app/gui_app.py
```

---

## 📜 License
This project is open-source.
