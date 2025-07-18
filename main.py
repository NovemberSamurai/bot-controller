import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import threading
from bot.application import run_bot
from health.server import app as health_app
from config.settings import PORT

def start_health():
    health_app.run(host='0.0.0.0', port=PORT)

if __name__ == '__main__':
    t = threading.Thread(target=start_health, daemon=True)
    t.start()
    run_bot()
