from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from use_case.heart.heart_processor import process_heart_rate_data, emit_heart_rate_data
import os
import ast

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
        data.append(ast.literal_eval(elem))
    if not data:
        return jsonify({"error": "Invalid input please upload a csv file for processing"}), 400
    try:
        error_message = process_heart_rate_data(data)
        return jsonify({"status": "File has been processed"}), 200
    except Exception as e:
        print(f"Following error occurred while processing heart rate data: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        socketio.start_background_task(target=emit_heart_rate_data, socketio=socketio)

@socketio.on('connect')
def handle_web_socket_connect(*args, **kwargs):
    print('Client connected')
    
@socketio.on('disconnect')
def handle_web_socket_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)