#!/bin/bash

# 1. Start the Flask app in the background
# The & allows the script to move to the next line immediately
python app.py &

# 2. Wait a few seconds to let Flask bind to the port
sleep 5

# 3. Start the Bot in the foreground
# This keeps the container alive
python bot.py
