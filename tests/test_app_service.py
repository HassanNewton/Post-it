import json
import importlib
from app.app import app as main_app


app_module = importlib.import_module("app.app")


def test_post_uses_data_service(monkeypatch):
    # avoid real rabbit: patch get_rabbit_connection
    class DummyChan:
        def queue_declare(self, *a, **k):
            pass
        def basic_publish(self, *a, **k):
            pass

    class DummyConn:
        def channel(self):
            return DummyChan()
        def close(self):
            pass

    monkeypatch.setattr(app_module, "get_rabbit_connection", lambda: DummyConn())

    # patch requests.post to emulate data-service
    class DummyResp:
        def __init__(self, code=201):
            self.status_code = code
        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception("bad")
        def json(self):
            return {"ok": True}

    monkeypatch.setattr(app_module.requests, "post", lambda *a, **k: DummyResp(201))

    client = main_app.test_client()
    r = client.post("/api/post", json={"author": "me", "message": "hi"})
    assert r.status_code == 200


def test_get_posts_calls_data_service(monkeypatch):
    monkeypatch.setattr(app_module.requests, "get", lambda *a, **k: type("R", (), {"status_code": 200, "raise_for_status": lambda self=None: None, "json": lambda self=None: [{"author": "a", "message": "b"}]})())
    client = main_app.test_client()
    r = client.get("/api/posts")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)
