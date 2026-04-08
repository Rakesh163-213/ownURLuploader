from flask import Flask
from threading import Thread

# == Flask App ==
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return '✅ Flask is running! Bot should be running too.'

def run_flask():
    flask_app.run(host='0.0.0.0', port=8000)

# Start Flask in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()
