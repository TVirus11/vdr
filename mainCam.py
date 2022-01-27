import cv2
import imutils
import numpy as np
import ChangeClothes as cc
import random
import urllib.request
import pygame

def capture():
    global bytes
    stream = urllib.request.urlopen('http://10.42.0.205:8080/video')
    bytes =  bytes()
    pygame.init()
    
    images = cc.loadImages()
    thres = [130, 40, 75, 130]
    size = 180
    curClothId = 1
    th = thres[0]
    
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2]
            cam = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            
            t_shirt = images[curClothId]
            resized = imutils.resize(cam, width=800)
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, r) in circles:
                    if r > 30:
                        cv2.circle(cam, (x, y), r, (0, 255, 0), 4)
                        cv2.rectangle(cam, (x-5, y-5), (x + 5, y+5), (0, 128, 255), -1)
                        size = r * 7
            if size > 350:
                size = 350
            elif size < 100:
                size = 100
                
            t_shirt = imutils.resize(t_shirt, width=size)
            
            f_height = cam.shape[0]
            f_width = cam.shape[1]
            t_height = t_shirt.shape[0]
            