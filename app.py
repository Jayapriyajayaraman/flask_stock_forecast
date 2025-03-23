import pandas as pd
from flask import Flask, render_template
from statsmodels.tsa.statespace.sarimax import SARIMAX

app = Flask(__name__)

# ✅ Load CSV instead of API
df = pd.read_csv("GME_stock.csv")
print("Columns in CSV:", df.columns)  # Debugging

# ✅ Check if "close_price" exists (instead of "close")
if "close_price" not in df.columns:
    raise ValueError("CSV file does not contain 'close_price' column.")

# ✅ Fix column name in function
def forecast_stock_prices(df):
    model = SARIMAX(df["close_price"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results = model.fit()
    forecast = results.get_forecast(steps=5)
    return forecast.predicted_mean

@app.route("/")
def home():
    forecasted_values = forecast_stock_prices(df)
    return render_template("index.html", forecast=forecasted_values)

if __name__ == "__main__":
    app.run(debug=True)

