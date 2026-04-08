#!/bin/bash

# 1. Start Tor in the background (if you're still using it)
tor > /dev/null &

# 2. Start the Flask app in the background
python app.py &

# 3. Start the Bot in the FOREGROUND
# This is the "Anchor." As long as this is running, 
# Koyeb will keep the whole instance alive.
python bot.py
