# Use a lightweight Python image
FROM python:3.10-slim

# Install FFmpeg and other necessary system tools
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements file first to take advantage of Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code into the container
COPY . .

# Ensure start.sh is executable (just in case)
RUN chmod +x start.sh

# Start the bot using your script
CMD ["sh", "start.sh"]
