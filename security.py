


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 13:41:07 2022

@author: nikhilsaini
"""

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
                            host='localhost',
                            port='5432')
    # Get the cursor object from the connection object
    print(conn)
    curr = conn.cursor()
    return conn, curr


def create_table():
    try:
        # Get the cursor object from the connection object
        conn, curr = create_connection()
        try:
            # Fire the CREATE query
            curr.execute("CREATE TABLE IF NOT EXISTS \
            cartoon(photoID INTEGER, name TEXT,\
            photoImg BYTEA)")
              
        except(Exception, psycopg2.Error) as error:
            # Print exception
            print("Error while creating cartoon table", error)
        finally:
            # Close the connection object
            conn.commit()
            conn.close()
    finally:
        # Since we do not have to do anything here we will pass
        pass
  
create_table()

def write_blob(photoID, file_path, name):
    try:
        # Read data from a image file
        drawing = open(file_path, 'rb').read()
        # Read database configuration
        conn, cursor = create_connection()
        try:           
            # Execute the INSERT statement
            # Convert the image data to Binary
            cursor.execute("INSERT INTO cartoon\
            (photoID,name,photoImg) " +
                    "VALUES(%s,%s,%s)",
                    (photoID,name, psycopg2.Binary(drawing)))
            # Commit the changes to the database
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while inserting data in cartoon table", error)
        finally:
            # Close the connection object
            conn.close()
    finally:
        # Since we do not have to do
        # anything here we will pass
        pass

create_connection()

cam = cv2.VideoCapture(0)
while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    #cv2.imshow('secu cam', diff)
    #cv2.waitKey(0)s
    
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ =cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #pyautogui.press("t")
        print("t")
        #os.system("say i see u, I am calling POLICE")
        start = time.time()
        photo_time = 4
        while time.time()  - start <= photo_time:
            
           _, photo = cam.read()
           myuuid = str(uuid.uuid4())
           cv2.imwrite("./photos/{0}.jpg".format(myuuid), photo)   
           
           integer = random.randint(0,10)
           write_blob(integer,"./photos/{0}.jpg".format(myuuid), myuuid)
           

           print(myuuid)
           time.sleep(4)
        
        
        #print(photo)
        
    #if cv2.waitKey(10) == ord('q'):
    #    break
    
    
    
  
