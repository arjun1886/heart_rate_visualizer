from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from use_case.heart.heart_processor import process_heart_rate_data, emit_heart_rate_data
import json
import os
import gevent.monkey
gevent.monkey.patch_all()
app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', logger=True, engineio_logger=True)

# Serving the HTML page
@app.route('/')
def index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'templates'), 'index.html')

# Serving static files (JavaScript, CSS)
"""@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)"""

@app.route('/process/csv', methods=['POST'])
def process_csv_file():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Invalid input please upload a csv file for processing"}), 400
    try:
        data = json.loads(json_data)
        process_heart_rate_data(data)
        return jsonify({"status": "File has been processed"}), 200
    except Exception:
        print(f"Error uploading file")
        return jsonify({"error": "Error uploading file, please try again later"}), 500

@socketio.on('connect')
def handle_web_socket_connect(*args, **kwargs):
    print('Client connected')
    emit_heart_rate_data(socketio)

@socketio.on('disconnect')
def handle_web_socket_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    #socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    server = WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()