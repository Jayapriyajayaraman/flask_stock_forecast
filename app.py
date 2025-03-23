import pandas as pd

# Load stock data
csv_file = "GME_stock.csv"
df = pd.read_csv(csv_file)

# Check if 'close_price' column exists
if "close_price" not in df.columns:
    print("Error: 'close_price' column not found in CSV.")
else:
    # Example forecast values (Replace with actual forecast logic if needed)
    forecast_values = [10.1, 10.2, 10.3, 10.4, 10.5]

    # Create DataFrame and save it
    forecast_df = pd.DataFrame(forecast_values, columns=["Forecasted Price"])
    print("Forecasted values:", forecast_df)  # Debugging
    forecast_df.to_csv("forecast.csv", index=False)
    print("✅ Forecast saved to forecast.csv")
import os
from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Load precomputed forecast
df = pd.read_csv("forecast.csv")

@app.route("/")
def home():
    forecast = df["Forecasted Price"].tolist()

    # Create static chart
    fig = px.line(df, y="Forecasted Price", title="Stock Price Forecast")
    graph_html = fig.to_html(full_html=False)

    return render_template("index.html", forecast=forecast, graph_html=graph_html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000
    app.run(debug=True, host="0.0.0.0", port=port)
