from flask import Flask, request, jsonify
import threading
import time
import requests

app = Flask(__name__)

target_url = None
rate = 0 
running = False

def workload_loop():
    global rate, target_url, running
    while running:
        start = time.time()
        for _ in range(rate):
            try:

                requests.post(target_url, json={"author": "author", "message": "message"}, timeout=1)
            except Exception as e:
                print(f"Request error: {e}")
        elapsed = time.time() - start
        if elapsed < 1:
            time.sleep(1 - elapsed)

@app.route("/workload", methods=["POST"])
def set_workload():
    global rate, target_url, running

    data = request.get_json()
    if not data or "url" not in data or "rate" not in data:
        return jsonify({"error": "Provide 'url' and 'rate' in JSON"}), 400

    target_url = data["url"]
    new_rate = int(data["rate"])

    if not running:
        running = True
        threading.Thread(target=workload_loop, daemon=True).start()

    rate = new_rate
    return jsonify({"status": "ok", "rate": rate, "url": target_url})

@app.route("/workload/stop", methods=["POST"])
def stop_workload():
    global running
    running = False
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    print("Starting external workload generator on port 5000")
    app.run(host="0.0.0.0", port=5000)
