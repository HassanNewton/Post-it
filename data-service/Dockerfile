FROM python:3.11-slim

WORKDIR /data-service

COPY app.py requirements.txt /data-service/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6000

CMD ["python3", "app.py"]
