from flask import Flask, render_template, request, jsonify
import os
import sys
import webbrowser
import threading  # For opening browser without blocking Flask

# -------------------------
# Force local nova_backend.py import
# -------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import nova_backend
    print("Using nova_backend from:", nova_backend.__file__)
    print("Available attributes:", dir(nova_backend))
except Exception as e:
    print("[ERROR] Could not import nova_backend:", e)
    raise e

# -------------------------
# DEBUG: Check templates folder
# -------------------------
print("Current working dir:", os.getcwd())
print("Templates folder exists:", os.path.exists("templates/index.html"))

app = Flask(__name__)

# -------------------------
# Home route - renders Nova interface
# -------------------------
@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        print("[ERROR] Could not render index.html:", e)
        return "Error loading interface. Check templates folder."

# -------------------------
# Command route - receives JS POST requests
# -------------------------
@app.route("/command", methods=["POST"])
def command():
    try:
        # Force JSON parsing in case headers are missing
        data = request.get_json(force=True)
        if not data or "command" not in data:
            print("[WARNING] No command received from frontend:", data)
            return jsonify({"response": "No command received"})

        query = data["command"]
        print("[DEBUG] Received command:", query)

        # Check if MainExecution exists before calling
        if not hasattr(nova_backend, "MainExecution"):
            print("[ERROR] nova_backend has no attribute MainExecution")
            return jsonify({"response": "Backend function MainExecution not found"})

        # Run backend command
        response = nova_backend.MainExecution(query)
        print("[DEBUG] Response:", response)

        return jsonify({"response": response})

    except Exception as e:
        print("[ERROR] Exception in /command:", e)
        return jsonify({"response": f"Error processing command: {e}"})


# -------------------------
# Function to open browser automatically
# -------------------------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


# -------------------------
# Main server start
# -------------------------
if __name__ == "__main__":
    print("Starting NOVA Server...")

    # Open browser in a separate thread to avoid blocking Flask
    threading.Timer(1.0, open_browser).start()

    # Run Flask server
    app.run(host="127.0.0.1", port=5000, debug=True)
