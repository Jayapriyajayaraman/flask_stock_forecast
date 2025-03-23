import os
import pandas as pd
from flask import Flask, jsonify
from statsmodels.tsa.statespace.sarimax import SARIMAX

app = Flask(__name__)

CSV_FILE = "GME_stock.csv"
FORECAST_FILE = "forecast.csv"

# ✅ Precompute forecast only once
def compute_forecast():
    try:
        df = pd.read_csv(CSV_FILE)

        if "close_price" not in df.columns:
            return "Error: 'close_price' column missing in CSV."

        # Train SARIMA model
        model = SARIMAX(df["close_price"], order=(1,1,1), seasonal_order=(1,1,1,12))
        results = model.fit()

        # Forecast next 5 days
        forecast = results.forecast(steps=5)
        forecast_df = pd.DataFrame(forecast, columns=["Forecasted Price"])

        # Save forecast data to CSV
        forecast_df.to_csv(FORECAST_FILE, index=False)
        print("✅ Forecast saved to forecast.csv")
    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run forecast computation before starting Flask
compute_forecast()

@app.route("/")
def home():
    return "📈 Stock Forecast App is Running!"

@app.route("/forecast")
def get_forecast():
    if not os.path.exists(FORECAST_FILE):
        return jsonify({"error": "Forecast file not found"}), 500
    
    df = pd.read_csv(FORECAST_FILE)
    return df.to_json(orient="records")

# ✅ Gunicorn-compatible start command
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
