# Use a Python base image with version 3.8
FROM python:3.8

# Set the timezone non-interactively
ENV TZ=UTC

# Set the working directory inside the container
WORKDIR /app

# Update package lists
RUN apt-get update

# Install the required Python packages
RUN pip install --no-cache-dir psycopg2 opencv-python-headless

# Install additional packages
RUN apt-get install -y \
    libmagic-dev \
    && apt-get clean

# Copy the application files into the container
COPY . .
