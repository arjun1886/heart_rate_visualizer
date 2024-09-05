from repository.persistence.my_sql import add_records
from repository.streaming.kafka.publisher import publish_heart_rate_data
from repository.streaming.kafka.subscriber import subscribe_to_heart_rate_data
from entities.error import ErrorMessage
import time

def persist_heart_data(data):
    message = add_records(data)
    if message == "":
       error_message = ErrorMessage(message,200)
    else:
       error_message = ErrorMessage("",500)
    return error_message

def emit_heart_rate_data(socketio):
   list_of_heart_rates = subscribe_to_heart_rate_data()
   old_data = {}
   for heart_rate_data in list_of_heart_rates:
       heart_rate_data = detect_heart_rate_anomaly(heart_rate_data, old_data)
       time.sleep(1)
       socketio.emit('heart_rate_data',heart_rate_data)
       old_data = heart_rate_data

def detect_heart_rate_anomaly(heart_rate_data, old_data):
   if heart_rate_data == "":
      heart_rate_data["anomaly"] = "Missing data"
      if old_data:
         heart_rate_data["heart_rate"] = old_data["heart_rate"]
   if old_data:
      if heart_rate_data["heart_rate"] - old_data["heart_rate"] > 30:
         heart_rate_data["anomaly"] = "Sudden spike in heart rate, could be a health concern"
      elif old_data["heart_rate"] - heart_rate_data["heart_rate"] < 30:
         heart_rate_data["anomaly"] = "Sudden dip in heart rate, could be a health concern"
   return heart_rate_data
    
def process_heart_rate_data(data):
   error_message = persist_heart_data(data)
   stream_heart_rate_data(data)
   return error_message

def stream_heart_rate_data(records):
   publish_heart_rate_data(records)
   

