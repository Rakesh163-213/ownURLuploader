from flask import Flask
from threading import Thread

# == Flask App ==
app = Flask(name)

@app.route('/')
def home():
    return '✅ Flask is running!'

def run_flask():
    app.run(host='0.0.0.0', port=8000)

# Start Flask in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()
