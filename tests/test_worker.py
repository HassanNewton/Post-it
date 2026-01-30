import pathlib


def test_worker_no_redis_import():
    text = pathlib.Path("worker/worker.py").read_text()
    assert "import redis" not in text


def test_worker_dockerfile_no_redis():
    docker = pathlib.Path("worker/Dockerfile").read_text()
    assert "redis" not in docker.lower()
