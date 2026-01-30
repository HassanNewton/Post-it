import json
from data_service.app import app as data_app


class FakeRedis:
    def __init__(self):
        self.kv = {}
        self.lists = {}

    def lpush(self, key, value):
        self.lists.setdefault(key, []).insert(0, value)

    def lrange(self, key, start, end):
        return self.lists.get(key, [])[start:end+1]

    def ltrim(self, key, start, end):
        self.lists[key] = self.lists.get(key, [])[start:end+1]

    def incr(self, key, amount=1):
        self.kv[key] = int(self.kv.get(key, 0)) + amount

    def set(self, key, val):
        self.kv[key] = val

    def get(self, key):
        return self.kv.get(key)


def test_posts_endpoint(monkeypatch):
    fake = FakeRedis()

    def fake_redis(*a, **k):
        return fake

    monkeypatch.setattr("data_service.app.redis.Redis", fake_redis)

    client = data_app.test_client()

    post = {"author": "me", "message": "hello"}
    r = client.post("/data/posts", json=post)
    assert r.status_code == 201

    r = client.get("/data/posts")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, list)
    assert data[0]["author"] == "me"


def test_processed_and_stats(monkeypatch):
    fake = FakeRedis()
    monkeypatch.setattr("data_service.app.redis.Redis", lambda *a, **k: fake)

    client = data_app.test_client()

    r = client.post("/data/processed", json={"value": "42"})
    assert r.status_code == 200

    r = client.get("/data/stats")
    assert r.status_code == 200
    stats = r.get_json()
    assert stats["total_processed"] == 1
    assert stats["last_value"] == "42"
    assert stats["recent_values"][0] == "42"
