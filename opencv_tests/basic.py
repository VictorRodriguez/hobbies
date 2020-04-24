import cv2 as cv
import requests
import os

file_name="messi5.jpg"
url = 'https://raw.githubusercontent.com/opencv/opencv/master/samples/data/messi5.jpg'
myfile = requests.get(url)
open(file_name, 'wb').write(myfile.content)

img = cv.imread('messi5.jpg')
px = img[100,100]
print(px)
os.remove(file_name)
