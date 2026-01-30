import importlib
from app.app import app
mod = importlib.import_module('app.app')
class R:
    def __init__(self):
        self.status_code = 200
    def raise_for_status(self):
        return None
    def json(self):
        return [{'author':'a','message':'b'}]

mod.requests.get = lambda *a, **k: R()
client = app.test_client()
r = client.get('/api/posts')
print('status', r.status_code)
print(r.get_data(as_text=True))
