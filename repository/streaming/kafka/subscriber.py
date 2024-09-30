from confluent_kafka import Consumer, KafkaException
import json
import time

def subscribe_to_heart_rate_data(socketio):
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'heart-rate-group',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe(['heart-rate-topic'])
    old_data = {}
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            
            # Deserialize JSON message
            heart_rate_data = json.loads(msg.value().decode('utf-8'))
            heart_rate_data = detect_heart_rate_anomaly(heart_rate_data, old_data)
            socketio.emit('heart_rate_data',heart_rate_data)
            socketio.sleep(1)
            old_data = heart_rate_data

    except KeyboardInterrupt:
        # Handle any cleanup or shutdown procedures if needed
        pass
    finally:
        consumer.close()

def detect_heart_rate_anomaly(heart_rate_data, old_data):
   if not heart_rate_data or not heart_rate_data["heart_rate"] or not heart_rate_data["timestamp"]:
      heart_rate_data["anomaly"] = "Missing data"
      heart_rate_data["heart_rate"] = 0.0
   elif old_data:
      if float(heart_rate_data["heart_rate"]) - float(old_data["heart_rate"]) > 30.0:
         heart_rate_data["anomaly"] = "Sudden spike in heart rate, could be a health concern"
      elif float(old_data["heart_rate"]) - float(heart_rate_data["heart_rate"]) > 30.0:
         heart_rate_data["anomaly"] = "Sudden dip in heart rate, could be a health concern"
      else:
         heart_rate_data["anomaly"] = None
   return heart_rate_data