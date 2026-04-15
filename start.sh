#!/bin/bash

# 1. Start Tor
#tor &
#sleep 20

# 2. Start Flask (using & to background it)
# We use 'python3' to be safe and ensure the path is clear
python3 /app/app.py &

# 3. Wait for Flask
sleep 5

# 4. Start the Bot (no & here, this keeps the container running)
python3 /app/bot.py
