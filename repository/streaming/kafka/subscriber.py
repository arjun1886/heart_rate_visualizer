from confluent_kafka import Consumer, KafkaException
import json

def subscribe_to_heart_rate_data():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'heart-rate-group',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['heart_rate_topic'])
    list_of_heart_rate_data = []

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            
            # Deserialize JSON message
            heart_rate_data = json.loads(msg.value().decode('utf-8'))
            list_of_heart_rate_data.append(heart_rate_data)

    except KeyboardInterrupt:
        # Handle any cleanup or shutdown procedures if needed
        pass
    finally:
        consumer.close()

    return list_of_heart_rate_data