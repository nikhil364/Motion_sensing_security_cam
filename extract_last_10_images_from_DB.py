#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 02:47:58 2023

@author: nikhilsaini
"""

import os
import psycopg2
from io import BytesIO
from PIL import Image

import cv2  
import os
#import pyautogui
import uuid
import time

import psycopg2
import random

def create_connection():
    # Connect to the database
    # using the psycopg2 adapter.
    # Pass your database name ,# username , password , 
    # hostname and port number
    conn = psycopg2.connect(dbname='photos',
                            user='root',
                            password='root',
                            host='postgres',
                            port='5432')
    # Get the cursor object from the connection object
    print(conn)
    curr = conn.cursor()
    return conn, curr

def extract_last_10_photos(output_directory):
    try:
        # Get the cursor object from the connection object
        conn, curr = create_connection()
        try:
            # Fetch the last 10 photos from the database, ordered by the database index
            curr.execute("SELECT photoID, name, photoImg FROM cartoon ORDER BY ctid DESC LIMIT 20")
            rows = curr.fetchall()

            # Create the output directory if it doesn't exist
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            # Save each photo to the output directory
            for row in rows:
                photo_id, name, photo_img = row
                image = Image.open(BytesIO(photo_img))
                image_path = os.path.join(output_directory, f"{name}_{photo_id}.png")
                image.save(image_path)
                print(f"Saved photo {photo_id} to {image_path}")

        except (Exception, psycopg2.Error) as error:
            # Print exception
            print("Error while extracting photos", error)

        finally:
            # Close the connection object
            conn.close()

    finally:
        # Since we do not have to do anything here we will pass
        pass

# Example usage:
output_directory = "./extracted_photos_for_viewing"
extract_last_10_photos(output_directory)
