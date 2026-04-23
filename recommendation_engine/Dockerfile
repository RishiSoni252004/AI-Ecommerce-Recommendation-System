FROM python:3.10-slim

WORKDIR /app

COPY recommendation_engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY recommendation_engine/ ./recommendation_engine/
COPY database/ ./database/
COPY kafka_stream/ ./kafka_stream/

ENV PYTHONPATH=/app

CMD ["python", "recommendation_engine/worker.py"]
