from confluent_kafka import Producer
import json
from entities.error import ErrorMessage

def publish_heart_rate_data(records) -> ErrorMessage:
    """
    Publish heart rate data to a Confluent Kafka topic.
    """
    # Kafka configuration
    conf = {
        'bootstrap.servers': 'localhost:9092',  # Kafka broker address
        'client.id': 'heart-rate-producer',     # Optional: a client identifier
        'acks': 'all'                           # Acknowledgment for message delivery (optional)
    }
    
    # Create a Producer instance
    producer = Producer(conf)
    error_message = ErrorMessage("",200)
    def delivery_report(err, msg):
        """
        Delivery callback to report success or failure of message delivery.
        """
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
    
    # Serialize and send the heart rate data to the Kafka topic
    try:
        for record in records:
            # Convert the record to JSON and send it
            producer.produce(
                'heart-rate-topic', 
                key=None,  # Optional: you can add keys for partitioning if needed
                value=json.dumps(record),
                callback=delivery_report  # Callback to check delivery status
            )
    except Exception as e:
        error_message.set_code(500)
        error_message.set_message(str(e))
        return error_message
    finally:
        # Wait for all messages to be delivered
        producer.flush()
        return error_message