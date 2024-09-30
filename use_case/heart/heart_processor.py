from repository.persistence.my_sql import add_records
from repository.streaming.kafka.publisher import publish_heart_rate_data
from repository.streaming.kafka.subscriber import subscribe_to_heart_rate_data
from entities.error import ErrorMessage
import time

def persist_heart_data(data):
    preprocessed_data = preprocess_heart_data(data)
    message = add_records(preprocessed_data)
    if message == "":
       error_message = ErrorMessage("",200)
    else:
       error_message = ErrorMessage(message,500)
    return error_message
    
def preprocess_heart_data(data):
    for i in range(len(data)):
        if data[i]["heart_rate"] == None or data[i]["heart_rate"] == "":
           data[i]["heart_rate"] = -1.0
    return data
     

def process_heart_rate_data(data):
   db_error_message = persist_heart_data(data)
   message = db_error_message.get_message()
   if message != "":
      return db_error_message 
   streaming_error_message = stream_heart_rate_data(data)
   return streaming_error_message

def stream_heart_rate_data(records):
   publish_error_message = publish_heart_rate_data(records)
   return publish_error_message
   

def emit_heart_rate_data(socketio):
    subscribe_to_heart_rate_data(socketio)
