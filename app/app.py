import os, json, time, sys, traceback
from flask import Flask, request, jsonify
import pika
import requests

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBIT_USER", "appuser")
RABBIT_PASS = os.getenv("RABBIT_PASS", "appsecret")
DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://data-service:6000")

app = Flask(__name__)

def get_rabbit_connection():
    creds = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    params = pika.ConnectionParameters(
    host=RABBIT_HOST,
    credentials=creds,
    heartbeat=30
    )
    return pika.BlockingConnection(params)

@app.route("/api/post", methods=["POST"])
def post_message():
    payload = request.get_json(force=True, silent=True) or {}
    author = payload.get("author")
    message = payload.get("message")

    if not author or not message:
        return jsonify({"error": "missing author or message"}), 400

    post = {
        "ts": time.time(),
        "author": author,
        "message": message
    }

    # send post to data-service
    try:
        resp = requests.post(f"{DATA_SERVICE_URL}/data/posts", json=post, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        return jsonify({"error": "failed to store post", "detail": str(e)}), 500

    conn = get_rabbit_connection()
    ch = conn.channel()
    ch.queue_declare(queue="jobs", durable=False)
    ch.basic_publish(exchange="", routing_key="jobs", body=json.dumps(post).encode("utf-8"))
    conn.close()

    return jsonify(post)

@app.route("/api/posts", methods=["GET"])
def get_posts():
    try:
        resp = requests.get(f"{DATA_SERVICE_URL}/data/posts", params={"limit": 50}, timeout=5)
        resp.raise_for_status()
        posts = resp.json()
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": "failed to fetch posts", "detail": str(e)}), 500
    return jsonify(posts)

@app.route("/", methods=["GET"])
def root():
    return jsonify({"ok": True, "msg": "PostIt board backend running"})

if __name__ == "__main__":
    print("Starting Flask on 0.0.0.0:5000", flush=True)
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)