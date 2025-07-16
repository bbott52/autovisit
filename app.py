from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import threading
import time

app = Flask(__name__)
CORS(app)

visit_url = None

def visit_loop():
    global visit_url
    while True:
        if visit_url:
            try:
                res = requests.get(visit_url)
                print(f"[{time.strftime('%H:%M:%S')}] ✅ Visited: {visit_url} | Status: {res.status_code}")
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] ❌ Error: {e}")
        time.sleep(2)

# Background thread
threading.Thread(target=visit_loop, daemon=True).start()

@app.route("/")
def home():
    return "✅ Auto Visitor is Running"

@app.route("/start", methods=["POST"])
def start():
    global visit_url
    data = request.get_json()
    visit_url = data.get("url")
    return jsonify({"message": f"🔁 Backend now visiting: {visit_url} every 2 seconds."})
