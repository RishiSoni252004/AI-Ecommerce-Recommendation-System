import os
import json
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable


def _build_consumer_config(kafka_broker: str, group_id: str) -> dict:
    """
    Builds KafkaConsumer kwargs.
    - Local / Docker: plain PLAINTEXT (no credentials needed)
    - Confluent Cloud / Azure Event Hubs: SASL_SSL with PLAIN mechanism
    Auto-detects based on presence of KAFKA_API_KEY env var.
    """
    config = {
        "bootstrap_servers": [kafka_broker],
        "auto_offset_reset": "earliest",
        "enable_auto_commit": True,
        "group_id": group_id,
        "value_deserializer": lambda x: json.loads(x.decode("utf-8")),
        "request_timeout_ms": 30000,
        "session_timeout_ms": 10000,
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
        print("Kafka consumer: Using SASL_SSL (Confluent Cloud / Azure Event Hubs mode)")
    else:
        print("Kafka consumer: Using PLAINTEXT (local / Docker mode)")

    return config


class ActivityConsumer:
    def __init__(self, group_id: str = "recsys_group"):
        self.kafka_broker = os.getenv("KAFKA_BROKER", "localhost:9092")
        self.topic = os.getenv("KAFKA_TOPIC", "user_activity_stream")
        self.consumer = None
        self._connect(group_id)

    def _connect(self, group_id: str):
        try:
            config = _build_consumer_config(self.kafka_broker, group_id)
            self.consumer = KafkaConsumer(self.topic, **config)
            print(f"✅ Kafka consumer connected to {self.kafka_broker}, topic={self.topic}")
        except NoBrokersAvailable:
            print(f"⚠️  Kafka broker not available at {self.kafka_broker}.")
            self.consumer = None
        except Exception as e:
            print(f"⚠️  Kafka consumer init failed: {e}")
            self.consumer = None

    def consume_events(self):
        """Yields decoded event dicts from Kafka. Handles consumer being None gracefully."""
        if self.consumer is None:
            print("Kafka consumer unavailable — no events will be consumed.")
            return
        for message in self.consumer:
            yield message.value
