"""
Real-time streaming components
Kafka-based event processing and feature engineering
"""

# from ..streaming.kafka_producer import KafkaProducer
from .feature_processor import FeatureProcessor

__all__ = ["KafkaProducer", "FeatureProcessor"]
