import numpy as np
import cv2 as cv
import argparse
import sys

cap = cv.VideoCapture(0)

if (cap.isOpened()== False): 
    print("\nUnable to read camera feed")

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Video capture timestamp (milliseconds)
    vTime = cap.get(0)
    # 0-based index of the frame to be decoded/captured next
    vFrame = cap.get(1)
    # Relative position of the video file: (0 to 1)
    vRelPos = cap.get(2)
    # Height and width of frame
    #vWid = cap.get(3)
    #vHi = cap.get(4)
    desiredWidth = 240
    desiredHeight = 180
    ret = cap.set(3,desiredWidth)
    ret = cap.set(4,desiredHeight)
    # Frame rate (in Hz)
    vFrameRate = cap.get(5)
    desiredFrameRate = 1/10
    #vFrameRate = cap.set(5,desiredFrameRate)
    # 4-character code of codec (I have no idea what this is)

    ret, Newframe = cap.read()



    cv.imshow('Frame',frame)
    cv.imshow('Grayscale',gray)
    cv.imshow('Modified Frame', ret)

    # Press Q on keyboard to exit
    if cv.waitKey(1000) & 0xFF == ord('q'):
        print("I closed because I said Q")
        break

# When everything done, release the video capture object
cap.release()
cv.destroyAllWindows()
