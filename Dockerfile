# Use the official Python image as a base
FROM debian:stable-slim

# Update package index and install Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-opencv \
    python3-psycopg2 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libfontconfig1 \
    libuuid1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app


