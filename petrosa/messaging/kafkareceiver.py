import os

from kafka import KafkaConsumer


def get_consumer(topic):
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=os.getenv(
                                 'KAFKA_SUBSCRIBER', 'localhost:9093'),
                             group_id=os.getenv(
                                 "NEW_RELIC_APP_NAME")
                             )

    return consumer