#!/usr/bin/env python3
import numpy as np
import cv2
import os
import sys
from os import path

pwd = os.getcwd()
cap = cv2.VideoCapture(0)

label = sys.argv[1]

dir_images = os.path.join(pwd, label)
print(dir_images)

if not path.isdir(dir_images):
    try:
        os.mkdir(dir_images)
    except OSError:
        print ("Creation of the directory %s failed" % dir_images)
else:
    print ("Directory %s exists" % dir_images)

ct = 0
maxCt = 5
print("Hit Space to Capture Image")

while True:
    ret, frame = cap.read()
    cv2.imshow('Get Data : '+label,frame[50:350,100:450])
    if cv2.waitKey(1) & 0xFF == ord(' '):
        cv2.imwrite(dir_images+'/'+label+'{}.jpg'.format(ct),frame[50:350,100:450])
        print(dir_images+'/'+label+'{}.jpg Captured'.format(ct))
        ct+=1
    if ct >= maxCt:
        break

cap.release()
cv2.destroyAllWindows()
