import os

from kafka import KafkaConsumer


def get_consumer(topic) -> KafkaConsumer:
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=os.getenv(
                                 'KAFKA_SUBSCRIBER', 'localhost:9093'),
                             group_id=os.getenv(
                                 "OTEL_SERVICE_NAME")
                             )

    return consumer