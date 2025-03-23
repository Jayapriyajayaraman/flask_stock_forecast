from flask import Flask, render_template
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

app = Flask(__name__)

# Load CSV File
df = pd.read_csv("GME_stock.csv")

def forecast_stock_prices(df):
    model = SARIMAX(df["close_price"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results = model.fit()
    forecast = results.get_forecast(steps=5).predicted_mean
    return forecast.tolist()

@app.route("/")
def home():
    forecasted_values = forecast_stock_prices(df)
    return render_template("index.html", stock="GME", forecast=forecasted_values)

if __name__ == "__main__":
    app.run(debug=True)
