# Build stage: Use Python 3.11/3.12 slim
FROM python:3.11-slim

# Install system dependencies (FFmpeg is the key for MP3/M4A support)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create uploads directory
RUN mkdir -p uploads && chmod 777 uploads

# Set environment variables
ENV PORT=5000
ENV FLASK_APP=backend/api.py

# Expose the port
EXPOSE 5000

# Run the application with Gunicorn for production
# We use 1 worker for the free tier to save memory
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 "backend.api:app"
