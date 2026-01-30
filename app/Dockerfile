FROM python:3.11-slim

WORKDIR /app

COPY app.py /app/

RUN pip install --no-cache-dir flask python-openstackclient pika requests

EXPOSE 5000

CMD ["python3", "app.py"]