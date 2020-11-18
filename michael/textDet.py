###############################################################
#
#   Program Description:  This program identifies text and
#       saves all text found on a screen in a series of strings
#       using OpenCV's EAST text detector and tesseract.
#
#   
#   Author: Michael Baldomero; mbaldome@purdue.edu
# 
############################################################## 

import cv2
import time # tic toc
import numpy
import argparse
import os
from imutils.object_detection import non_max_suppression
import pytesseract
import nms_mod

# build arguments and parse
parse = argparse.ArgumentParser()
parse.add_argument("--image",type=str,help="image to detect text on")
parse.add_argument("--east",type=str,help="path to EAST detector",
  default="frozen_east_text_detection.pb")
parse.add_argument("--confidence",type=float,default=0.5,
  help="minimum probability required to inspect region")
parse.add_argument("--width",type=int,default=320,
  help="resized image width (multiple of 32)")
parse.add_argument("--height",type=int,default=320,
  help="resized image height (multiple of 32)")
args = vars(parse.parse_args())

# input validation for image
if not os.path.isfile(args["image"]):
  print("\n[ERROR] Image not found!\n")
  exit(0)

if not os.path.isfile(args["east"]):
  print("\n[ERROR] Pretrained EAST not found!\n")
  exit(0)

print("\n[INFO] Image selected: "+args["image"]+"\n")

## Initialization
# load image, grab dimensions
image = cv2.imread(args["image"])
(origH, origW) = image.shape[:2]
original = image.copy() # make copy
original = cv2.GaussianBlur(original,(3,3),0) # blur for EAST and OCR
# original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB) # tesseract assumes rgb

## Recognition
# resize original (EAST only works with DIMS % 32 = 0)
image = cv2.resize(image, (args["width"], args["height"]))
bw = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
bw = cv2.adaptiveThreshold(bw,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
  cv2.THRESH_BINARY,13,2)
(h, w) = image.shape[:2]

# make a blob from image and forward pass it to EAST
# create layers to be putlled from EAST as (scores, geometry)
blob = cv2.dnn.blobFromImage(image, 1.0, (w,h), 
  (123.68, 116.78, 103.94), swapRB=True, crop=False)

layers = ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"]

tic = time.time() # 1
network = cv2.dnn.readNet(args["east"]) # load pretrained EAST for detection
toc = time.time() # 1
print("[INFO] Loading neural network took {:.3f} seconds".format(toc-tic))
tic = time.time() # 2
network.setInput(blob) # toss blob to network
toc = time.time() # 2
print("[INFO] Blob input took {:.3f} seconds".format(toc-tic))
tic = time.time() # 3
(scores, geometry) = network.forward(layers) # network output
toc = time.time() # 3
print("[INFO] Text detection took {:.3f} seconds".format(toc-tic))

# calculate bounding box and probability score for each text
(r, c) = scores.shape[2:4]
rectangles = [] # init bound box coords for each text region
confidence = [] # init confidence for text region, parallel with rectangles
angles = [] # init 

tic = time.time()
# compute boundary boxes
for y in range(0,r):
  scoreData = scores[0,0,y]
  x0 = geometry[0,0,y] 
  x1 = geometry[0,1,y]
  x2 = geometry[0,2,y]
  x3 = geometry[0,3,y]
  angle = geometry[0,4,y]

  for x in range(0,c):
    if scoreData[x] < args["confidence"]:
      continue

    theta = angle[x]
    xEnd = int(4.0*x + (x1[x]*numpy.cos(angle[x])) + (x2[x]*numpy.sin(angle[x])))
    yEnd = int(4.0*y - (x1[x]*numpy.sin(angle[x])) + (x2[x]*numpy.cos(angle[x]))) 
    xStart = int(xEnd - x1[x] - x3[x])
    yStart = int(yEnd - x0[x] - x2[x])

    rectangles.append((xStart, yStart, xEnd, yEnd, theta))
    # angles.append(angle[x])
    confidence.append(scoreData[x])
toc = time.time()
print("[INFO] Boundary boxes took {:.3f} seconds".format(toc-tic))

tic = time.time()
boxes = non_max_suppression(numpy.array(rectangles),probs=confidence,overlapThresh=0.7)
# boxes = nms_mod.non_max_suppression(numpy.array(rectangles),probs=confidence,overlapThresh=0.7)
toc = time.time()
print("[INFO] Non-Maximum-Suppresion took {:.3f} seconds".format(toc-tic))

## Detection
solutions = []

# set tesseract executable to PATH (use full path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
configuration = r'out_tsv --psm 7 bonsai_config tsv'
tic = time.time()
phi = 0.2
for (xStart, yStart, xEnd, yEnd, theta) in boxes:
  boxWidth = xEnd - xStart
  boxHeight = yEnd - yStart
  xStart = int(xStart * (origW / float(args["width"])))# - 0.05*boxWidth)
  yStart = int(yStart * (origH / float(args["height"])))# - 0.05*boxHeight)
  xEnd = int(xEnd * (origW / float(args["width"])))# + 0.05*boxWidth)
  yEnd = int(yEnd * (origH / float(args["height"])))# + 0.05*boxHeight)

  xStart1 = int(xStart - phi*boxWidth)
  yStart1 = int(yStart - phi*boxHeight)
  xEnd1 = int(xEnd + phi*boxWidth)
  yEnd1 = int(yEnd + phi*boxHeight)

  print(str(xStart1)+ " "+str(yStart1)+ " "+str(xEnd1)+ " "+str(yEnd1))
  print(str(theta))

  region = cv2.cvtColor(original[yStart1:yEnd1, xStart1:xEnd1], cv2.COLOR_BGR2GRAY)
  region = cv2.threshold(region,0, 255,
    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
  region_gray = cv2.cvtColor(region, cv2.COLOR_GRAY2BGR)

  # cv2.imshow("box", region_gray)
  # cv2.waitKey(0)

  text = pytesseract.image_to_string(region_gray, config=configuration)#"tesseract_config.cfg")
  print(text)
  solutions.append(((xStart, yStart, xEnd, yEnd), text))

  # text = "".join([x if ord(x) < 128 else "" for x in text]).strip()
  cv2.putText(original, text, (xStart, yStart),
		cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,0, 255), 2)

  cv2.rectangle(original, (xStart, yStart),  (xEnd, yEnd), (0,255,0), 2)
  cv2.rectangle(original, (xStart1,yStart1), (xEnd1,yEnd1),(255,0,0), 2)
  # cv2.circle(original,(xStart,yStart), 5, (255,0,0), -1)
  # cv2.circle(original,(xEnd,yEnd),5,(0,0,255),-1)
toc = time.time()
print("[INFO] Text recognition took {:.3f} seconds".format(toc-tic))

print("\n") # newline
cv2.imshow(args["image"], original)
cv2.waitKey(0)