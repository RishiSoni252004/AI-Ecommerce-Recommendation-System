import time
import os
from kafka.errors import NoBrokersAvailable

# Ensure imports work with PYTHONPATH=/app
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recommendation_engine.model import HybridRecommender
from kafka_stream.consumer import ActivityConsumer


def run_worker():
    print("🚀 Initializing Recommendation Engine Worker...")
    recommender = HybridRecommender()

    # Retry loop: Kafka may not be ready immediately in cloud environments
    consumer = None
    for attempt in range(10):
        print(f"Connecting to Kafka (attempt {attempt + 1}/10)...")
        consumer = ActivityConsumer()
        if consumer.consumer is not None:
            print("✅ Kafka consumer connected. Listening for events...")
            break
        print(f"Kafka not ready. Retrying in 15s...")
        time.sleep(15)

    if consumer is None or consumer.consumer is None:
        print("❌ Could not connect to Kafka after 10 attempts. Worker exiting.")
        return

    for event in consumer.consume_events():
        print(f"📨 Received event: {event}")
        try:
            recommender.process_new_event(event)
        except Exception as e:
            print(f"⚠️  Error processing event: {e}")


if __name__ == "__main__":
    # Brief startup delay to allow dependent services to initialize
    startup_delay = int(os.getenv("WORKER_STARTUP_DELAY", "10"))
    print(f"Worker sleeping {startup_delay}s before startup...")
    time.sleep(startup_delay)
    run_worker()
