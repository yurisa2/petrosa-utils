import os

from kafka import KafkaProducer


def get_producer():
    producer = KafkaProducer(bootstrap_servers=os.getenv(
                                 'KAFKA_SUBSCRIBER', 'localhost:9092'),
                             client_id=os.getenv(
                                 "NEW_RELIC_APP_NAME")
                             )

    return producer