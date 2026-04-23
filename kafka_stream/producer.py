import os
import json
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


def _build_producer_config(kafka_broker: str) -> dict:
    """
    Builds KafkaProducer kwargs.
    - Local / Docker: plain PLAINTEXT (no credentials needed)
    - Confluent Cloud / Azure Event Hubs: SASL_SSL with PLAIN mechanism
    Auto-detects based on presence of KAFKA_API_KEY env var.
    """
    config = {
        "bootstrap_servers": [kafka_broker],
        "value_serializer": lambda v: json.dumps(v).encode("utf-8"),
        "request_timeout_ms": 10000,
        "retries": 3,
    }

    kafka_api_key = os.getenv("KAFKA_API_KEY")
    kafka_api_secret = os.getenv("KAFKA_API_SECRET")

    if kafka_api_key and kafka_api_secret:
        config.update({
            "security_protocol": "SASL_SSL",
            "sasl_mechanism": "PLAIN",
            "sasl_plain_username": kafka_api_key,
            "sasl_plain_password": kafka_api_secret,
        })
        print("Kafka: Using SASL_SSL (Confluent Cloud / Azure Event Hubs mode)")
    else:
        print("Kafka: Using PLAINTEXT (local / Docker mode)")

    return config


class ActivityProducer:
    def __init__(self):
        self.kafka_broker = os.getenv("KAFKA_BROKER", "localhost:9092")
        self.topic = os.getenv("KAFKA_TOPIC", "user_activity_stream")
        self.producer = None
        self._connect()

    def _connect(self):
        try:
            config = _build_producer_config(self.kafka_broker)
            self.producer = KafkaProducer(**config)
            print(f"✅ Kafka producer connected to {self.kafka_broker}, topic={self.topic}")
        except NoBrokersAvailable:
            print(f"⚠️  Kafka broker not available at {self.kafka_broker}. Events will be dropped.")
            self.producer = None
        except Exception as e:
            print(f"⚠️  Kafka producer init failed: {e}. Events will be dropped.")
            self.producer = None

    def send_event(self, event_data: dict):
        if self.producer is None:
            print(f"Kafka unavailable — dropping event: {event_data}")
            return
        try:
            self.producer.send(self.topic, event_data)
            self.producer.flush(timeout=5)
        except Exception as e:
            print(f"Kafka send error: {e}")


activity_producer = ActivityProducer()
