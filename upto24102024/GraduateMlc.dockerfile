FROM python:3.9-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the environment variable for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromium-driver

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY GraduateMlc.py ./