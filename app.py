import requests
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from flask import Flask, render_template
from statsmodels.tsa.statespace.sarimax import SARIMAX

app = Flask(__name__)

# MarketStack API details
API_KEY = "6784ad48df3cdd1aee293285fcd09145"
STOCK_SYMBOL = "AAPL"  # Change to any stock symbol

# Function to fetch stock data
def fetch_stock_data():
    url = f"http://api.marketstack.com/v1/eod?access_key={API_KEY}&symbols={STOCK_SYMBOL}&limit=100"
    response = requests.get(url).json()

    print("API Response:", response)  # Debugging line to check what the API returns

    if "data" not in response:
        return None  # Handle missing 'data' gracefully

    data = response["data"]
    df = pd.DataFrame(data)[["date", "close"]]
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    return df.sort_index()

# Train SARIMA model and forecast
def forecast_stock_prices(df, days=5):
    model = SARIMAX(df["close"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=days)
    return forecast

@app.route("/")
def home():
    df = fetch_stock_data()
    forecast = forecast_stock_prices(df)

    # Plotly chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["close"], mode="lines", name="Historical Prices"))
    future_dates = pd.date_range(start=df.index[-1], periods=len(forecast) + 1, freq="D")[1:]
    fig.add_trace(go.Scatter(x=future_dates, y=forecast, mode="lines", name="Forecasted Prices"))

    chart = fig.to_html(full_html=False)

    return render_template("index.html", chart=chart, stock=STOCK_SYMBOL)

if __name__ == "__main__":
    app.run(debug=True)

