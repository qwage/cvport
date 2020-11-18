import bonsai #custom functions
import cv2
import argparse
import keyboard
import pytesseract
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",type=str,required=True,help="path to video")
ap.add_argument("-east","--east",type=str,default="frozen_east_text_detection.pb")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="EAST Detector confidence")
args = vars(ap.parse_args())

bonsai.validate(args)

vid = cv2.VideoCapture(args["video"])
# frameSkip = 1 # will only do work on every frameSkip frames

## initialize layers and neural network for EAST
class detector: # I should rewrite this to be a dictionary
    layers =  ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"]
    confidence = args["confidence"]
    network = cv2.dnn.readNet(args["east"])

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
config = r'--oem 3 -l eng --psm 13 -c teddedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
size = sys.getsizeof(detector) + sys.getsizeof(pytesseract)

print("[INFO] DNN and OCR Size = " + str(size) + " MB")

solution = [] # initialize solutions array

ct = 0 # frame counter
while(vid.isOpened()):
    (ret, frame) = vid.read()  # capture each frame
    if ret == True:
        ct += 1
        frame = cv2.resize(frame, (960,512))

        if keyboard.is_pressed(' '): # detect text only on space press
            print("[INFO] Detection and OCR ran at frame " + str(ct))
            frame = bonsai.prepEAST(frame) # prep frame to be passed to EAST
            boxes = bonsai.passEAST(frame,detector) # pass frame to EAST and get bounding boxes
            frame = bonsai.postEAST(frame,boxes) # overlay boudning boxes onto image
            
            solution = bonsai.ocr(frame, boxes, config)

            for ((xStart, yStart, xEnd, yEnd),text) in solution:
                cv2.putText(frame, text, (xStart, yStart),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,0, 255), 2)
                print("[OCR] " + text)

            cv2.imshow("Read Frame " + str(ct), frame)

        cv2.imshow('Video Capture - press (q) to quit',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break # break if q is pressed

    else:
        print("[INFO] No more frames returned" if ct else "[INFO] Failed to load first frame")
        break # break once video is over

vid.release()
cv2.destroyAllWindows()

