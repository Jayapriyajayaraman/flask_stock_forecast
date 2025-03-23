from flask import Flask, render_template
from flask_socketio import SocketIO
import os

# Create Flask app
app = Flask(__name__)
socketio = SocketIO(app)  # Initialize Flask-SocketIO

@app.route("/")
def index():
    return render_template("index.html")

# Ensure `app` is defined before using it
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT not set
    socketio.run(app, debug=True, host="0.0.0.0", port=port)
