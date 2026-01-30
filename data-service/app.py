import os
import json
from flask import Flask, request, jsonify
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

app = Flask(__name__)


def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.route("/data/posts", methods=["POST"])
def post_post():
    payload = request.get_json(force=True, silent=True) or {}
    author = payload.get("author")
    message = payload.get("message")
    ts = payload.get("ts")

    if not author or not message:
        return jsonify({"error": "missing author or message"}), 400

    post = {"author": author, "message": message, "ts": ts or __import__("time").time()}

    r = get_redis()
    r.lpush("posts", json.dumps(post))

    return jsonify(post), 201


@app.route("/data/posts", methods=["GET"])
def get_posts():
    limit = int(request.args.get("limit", 50))
    r = get_redis()
    recent = r.lrange("posts", 0, limit - 1)
    posts = [json.loads(p) for p in recent]
    return jsonify(posts)


@app.route("/data/processed", methods=["POST"])
def post_processed():
    payload = request.get_json(force=True, silent=True) or {}
    value = payload.get("value")
    if value is None:
        return jsonify({"error": "missing value"}), 400

    r = get_redis()
    r.incr("total_processed", amount=1)
    r.lpush("recent_values", value)
    r.ltrim("recent_values", 0, 99)
    r.set("last_value", value)

    return jsonify({"ok": True}), 200


@app.route("/data/stats", methods=["GET"])
def get_stats():
    r = get_redis()
    total = r.get("total_processed") or "0"
    last = r.get("last_value")
    recent = r.lrange("recent_values", 0, 99)

    return jsonify({
        "total_processed": int(total),
        "last_value": last,
        "recent_values": recent,
    })


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    print("Starting data-service on 0.0.0.0:6000", flush=True)
    app.run(host="0.0.0.0", port=6000, debug=False, use_reloader=False)
