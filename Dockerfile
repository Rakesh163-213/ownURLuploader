FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg jq python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip first
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

# Check dependencies, skip yt-dlp check if not necessary
RUN python3 -m pip check
# Ensure start.sh is executable (just in case)
RUN chmod +x start.sh

# Start the bot using your script
#CMD ["sh", "start.sh"]
CMD ["/bin/bash", "start.sh"]
