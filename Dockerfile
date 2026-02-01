FROM python:3.12-slim

# Install FFmpeg and required dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway will set PORT env variable)
EXPOSE 8080

# Run the application
CMD gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300 --workers 2
