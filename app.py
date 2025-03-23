import os
import pandas as pd
from flask import Flask

app = Flask(__name__)

@app.route("/debug")
def debug():
    try:
        files = os.listdir(".")
        if "forecast.csv" in files:
            df = pd.read_csv("forecast.csv")
            return f"✅ `forecast.csv` found! <br><br> {df.to_html()}"
        else:
            return "❌ `forecast.csv` NOT found in the server directory!"
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
