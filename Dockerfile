FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-dev \
    build-essential \
    git \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY yamnet/ yamnet/
COPY *.py .
COPY *.sh .
COPY *.md .

# Make scripts executable
RUN chmod +x *.sh

# Run the text-only version (no GUI for Docker)
CMD ["python", "realtime_YAMNET_text.py"]

