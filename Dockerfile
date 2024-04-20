# Use Ubuntu as the base image
FROM ubuntu:20.04

# Update package lists and install Python 3.8 and pip
RUN apt-get update && \
    apt-get install -y python3.8 python3.8-dev python3-pip

# Install psycopg2 dependencies
RUN apt-get install -y libpq-dev

# Install OpenCV2 dependencies
RUN apt-get install -y libopencv-dev python3-opencv

# Set Python 3.8 as the default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# Install required Python packages
RUN pip3 install psycopg2 opencv-python-headless uuid

# Set the working directory
WORKDIR /app

# Copy the application files into the container
COPY . /app


