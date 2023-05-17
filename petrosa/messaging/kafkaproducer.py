import os

from kafka import KafkaProducer


def get_producer():
    producer = KafkaProducer(bootstrap_servers=os.getenv(
        'KAFKA_ADDRESS', 'localhost:9092'),
                             client_id=os.getenv(
                                 "OTEL_SERVICE_NAME")
                             )

    return producer