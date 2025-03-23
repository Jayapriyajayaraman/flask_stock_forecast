from flask import Flask, render_template
import pandas as pd
import os
import plotly.express as px

app = Flask(__name__)

@app.route("/")
def home():
    # Ensure forecast.csv exists
    if not os.path.exists("forecast.csv"):
        return "❌ Error: forecast.csv not found!"

    # Load forecasted data
    df = pd.read_csv("forecast.csv")

    # Convert to list for rendering in HTML
    forecast = df["Forecasted Price"].tolist()

    # Generate a Plotly static chart
    fig = px.line(df, y="Forecasted Price", title="Stock Price Forecast")
    graph_html = fig.to_html(full_html=False)

    return render_template("index.html", forecast=forecast, graph_html=graph_html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
