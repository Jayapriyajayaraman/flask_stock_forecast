from flask import Flask, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Load precomputed forecast
forecast_file = "forecast.csv"

@app.route("/")
def home():
    return "Stock Price Forecasting API is Live!"

@app.route("/forecast")
def get_forecast():
    if os.path.exists(forecast_file):
        forecast_df = pd.read_csv(forecast_file)
        return forecast_df.to_json(orient="records")
    else:
        return jsonify({"error": "Forecast data not found!"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
