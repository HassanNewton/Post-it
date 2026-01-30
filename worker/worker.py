import os, json, time, sys
import pika
import requests

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBIT_USER", "appuser")
RABBIT_PASS = os.getenv("RABBIT_PASS", "appsecret")
DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://data-service:6000")

creds = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
params = pika.ConnectionParameters(host=RABBIT_HOST, credentials=creds, heartbeat=30)
conn = None

while True:
    try:
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.queue_declare(queue="jobs", durable=False)

        def on_msg(ch, method, properties, body):
          try:
            msg = json.loads(body.decode("utf-8"))
            val = msg.get("value")
            if val is not None:
              x = 0
              for i in range(500000):
                  x += i * i % 7
              # send processed value to data-service
              try:
                resp = requests.post(f"{DATA_SERVICE_URL}/data/processed", json={"value": val}, timeout=5)
                resp.raise_for_status()
                print(f"Processed: {val}", flush=True)
              except Exception as e:
                print(f"ERR reporting to data-service: {e}", file=sys.stderr, flush=True)
          except Exception as e:
            print(f"ERR processing: {e}", file=sys.stderr, flush=True)

        ch.basic_consume(queue="jobs", on_message_callback=on_msg, auto_ack=True)
        print("Worker consuming...")
        ch.start_consuming()
    except Exception as e:
        print(f"Worker connection error: {e}. Retrying in 2s", file=sys.stderr, flush=True)
        time.sleep(2)