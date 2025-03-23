import pandas as pd
import plotly.graph_objects as go
from flask import Flask, render_template
from statsmodels.tsa.statespace.sarimax import SARIMAX

app = Flask(__name__)

# Load CSV file
df = pd.read_csv("GME_stock.csv")

def forecast_stock_prices(df):
    model = SARIMAX(df["close_price"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    results = model.fit()
    forecast = results.get_forecast(steps=5)
    return forecast.predicted_mean

@app.route("/")
def home():
    forecasted_values = forecast_stock_prices(df)

    # Create a static chart using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=forecasted_values, mode='lines+markers', name='Forecasted Prices'))
    graph_html = fig.to_html(full_html=False)

    return render_template("index.html", forecast=forecasted_values, graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)
