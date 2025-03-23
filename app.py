from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Load precomputed forecast data
df = pd.read_csv("forecast.csv")

# Create a Plotly chart
fig = px.line(df, y="Forecasted Price", title="Stock Price Forecast")
graph_html = fig.to_html(full_html=False)

@app.route("/")
def home():
    forecast = df["Forecasted Price"].tolist()
    return render_template("index.html", forecast=forecast, graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)
