FROM python:3.11-slim

WORKDIR /worker

COPY worker.py /worker/

RUN pip install --no-cache-dir pika requests

CMD ["python3", "worker.py"]