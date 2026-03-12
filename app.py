import os
import sys
import threading
from flask import Flask, render_template, request, jsonify
import webview
import time

# -------------------------
# Force local nova_backend.py import
# -------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import nova_backend
except Exception as e:
    print("[ERROR] Could not import nova_backend:", e)
    raise e

# -------------------------
# Flask app
# -------------------------
app = Flask(__name__)

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"Error loading interface: {e}"

@app.route("/command", methods=["POST"])
def command():
    try:
        data = request.get_json(force=True)
        if not data or "command" not in data:
            return jsonify({"response": "No command received"})

        query = data["command"]
        if not hasattr(nova_backend, "MainExecution"):
            return jsonify({"response": "Backend function MainExecution not found"})

        response = nova_backend.MainExecution(query)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"Error processing command: {e}"})

# -------------------------
# Flask server in background thread
# -------------------------
def start_flask():
    app.run(host="127.0.0.1", port=5000, debug=False)

# -------------------------
# Main: Start server and WebView
# -------------------------
if __name__ == "__main__":
    # Start Flask in a daemon thread
    threading.Thread(target=start_flask, daemon=True).start()

    # Wait for Flask to start
    time.sleep(2)  # 2 seconds should be enough for small apps

    # Fixed port 5000
    url = "http://127.0.0.1:5000"

    # Start native window (this blocks until window closed)
    webview.create_window(
        "NOVA Interface",
        url,
        width=1200,
        height=800,
        resizable=True
    )
    webview.start()