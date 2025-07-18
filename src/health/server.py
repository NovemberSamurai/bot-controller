import time
from flask import Flask, jsonify

app = Flask(__name__)
start_time = time.time()
message_count = 0
last_message_time = None

@app.route('/')
def info():
    return jsonify({
        'service': 'telegram-bot',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    uptime = time.time() - start_time
    return jsonify({
        'status': 'running',
        'uptime_seconds': uptime,
        'last_message_time': last_message_time,
        'message_count': message_count,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S')
    })
