from kafka import KafkaProducer
import json

def publish_heart_rate_data(records):
    """
    Publish heart rate data to a Kafka topic.
    """
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    for record in records:
        producer.send('heart_rate_topic', record)
        producer.flush()
