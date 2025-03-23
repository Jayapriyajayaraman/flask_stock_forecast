import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Ensure correct port binding
    app.run(debug=True, host="0.0.0.0", port=port)
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Stock Price Forecasting API is Live!"

# Ensure this is at the bottom of the file
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)
