from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from use_case.heart.heart_processor import process_heart_rate_data, emit_heart_rate_data
import json
import os
import asyncio

#import eventlet
#eventlet.monkey_patch()

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Serving the HTML page
@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'templates'), 'index.html')

@app.route('/process/csv', methods=['POST'])
def process_csv_file():
    json_data = request.get_json()
    data = []
    for elem in json_data:
        elem = str(elem).replace("'", "\"")
        elem = elem.replace("\\r", "")
        data.append(json.loads(elem))
    if not data:
        return jsonify({"error": "Invalid input please upload a csv file for processing"}), 400
    try:
        error_message = process_heart_rate_data(data)
        print(error_message.get_message)
        return jsonify({"status": "File has been processed"}), 200
    except Exception as e:
        print(f"Error uploading file")
        return jsonify({"error": str(e)}), 500

@socketio.on('connect')
def handle_web_socket_connect(*args, **kwargs):
    print('Client connected')

@socketio.on('file_uploaded')
def handle_file_uploaded(*args, **kwargs):
    emit_heart_rate_data(socketio)

@socketio.on('disconnect')
def handle_web_socket_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
    """server = WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()"""