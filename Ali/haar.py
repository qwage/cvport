import numpy as np
import cv2
#import psutil
from picamera.array import PiRGBArray
from picamera import PiCamera

haar_cascade_face = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
#full_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
#eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

#cap = cv2.VideoCapture(0) 
camera = PiCamera()
cap = PiRGBArray(camera)

while (1):
    #ret, img = cap.read()
    gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
    faces = haar_cascade_face.detectMultiScale(gray, 1.3, 5)
    #full = full_cascade.detectMultiScale(gray, 1.1, 5)
    #eye = eye_cascade.detectMultiScale(gray, 1.1, 5)
    
    for (x,y,w,h) in faces:
        cv2.rectangle(cap,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = cap[y:y+h, x:x+w]
    '''
    for (x,y,w,h) in full:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray1 = gray[y:y+h, x:x+w]
        roi_color1 = img[y:y+h, x:x+w]
    '''
    '''
    for (x,y,w,h) in eye:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray2 = gray[y:y+h, x:x+w]
        roi_color2 = img[y:y+h, x:x+w]
    '''
    cv2.imshow('img',cap)
    #print(psutil.virtual_memory().percent)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

