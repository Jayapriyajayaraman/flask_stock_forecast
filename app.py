import pandas as pd
from flask import Flask, render_template
from statsmodels.tsa.statespace.sarimax import SARIMAX

app = Flask(__name__)

# Load CSV file
try:
    df = pd.read_csv("GME_stock.csv")
    print("CSV Columns:", df.columns)  # Debugging
    print("First 5 Rows:\n", df.head())  # Debugging
    
    if "close_price" not in df.columns:
        raise ValueError("CSV file does not contain 'close_price' column.")
except Exception as e:
    print("Error loading CSV:", e)
    df = None

# Forecasting Function
def forecast_stock_prices(df):
    model = SARIMAX(df["close_price"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results = model.fit()
    forecast = results.get_forecast(steps=5)
    return forecast.predicted_mean

@app.route("/")
def home():
    if df is None:
        return "Error: Data not loaded properly. Check server logs."
    
    forecasted_values = forecast_stock_prices(df)
    return render_template("index.html", forecast=forecasted_values)

if __name__ == "__main__":
    app.run(debug=True)
