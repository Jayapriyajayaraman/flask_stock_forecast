import os
import time
import random
import pandas as pd
import plotly.express as px
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")

# Load initial stock data
csv_file = "GME_stock.csv"
df = pd.read_csv(csv_file)

# Generate initial forecast (Simulate API or Use Precomputed Data)
forecast_values = list(df["close_price"].tail(5)) if "close_price" in df.columns else [10.1, 10.2, 10.3, 10.4, 10.5]

@app.route("/")
def home():
    return render_template("index.html")

# Real-time data update function
def generate_live_data():
    """Simulates real-time stock updates every 2 seconds."""
    while True:
        new_value = forecast_values[-1] + random.uniform(-0.2, 0.2)  # Simulated stock movement
        forecast_values.append(new_value)
        
        # Keep only the last 10 values
        live_data = forecast_values[-10:]

        # Create updated chart
        df_live = pd.DataFrame({"Index": list(range(len(live_data))), "Forecasted Price": live_data})
        fig = px.line(df_live, x="Index", y="Forecasted Price", title="Live Stock Price Forecast")
        graph_html = fig.to_html(full_html=False)

        # Send updated data to frontend
        socketio.emit("update_chart", {"forecast": live_data, "graph_html": graph_html})

        time.sleep(2)  # Wait 2 seconds before next update

# Start background thread for live updates
@socketio.on("connect")
def handle_connect():
    socketio.start_background_task(generate_live_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, debug=True, host="0.0.0.0", port=port)
