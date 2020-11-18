import time
import numpy
from imutils.object_detection import non_max_suppression
import os
import cv2
import pytesseract

## Validate that Video and EAST are passed
def validate(args):
    if not os.path.isfile(args["video"]):
        print("\n[ERROR] Video not found!\n")
        exit(0)

    if not os.path.isfile(args["east"]):
        print("\n[ERROR] Pretrained EAST not found!\n")
        exit(0)

    print("\n[INFO] Video selected "+args["video"]+"\n")

## prep image for EAST (resize, blur, adaptive threshold, return)
##      EAST can only work with images that have dimensions that are
##      multiples of 32, so this just decreases image size to nearest
##      multiple of 32
def prepEAST(image):
    alpha = 1.25 # contrast control
    beta = 0.0 # brightness control

    # (h, w) = image.shape[:2]
    # image = cv2.resize(image, (w - w%32, h - h%32)) # resize image to 32 x 32 multiple dims
    image = cv2.convertScaleAbs(image,alpha=alpha,beta=beta)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)    
    # image = cv2.GaussianBlur(image,(3,3),0)
    
    return image

def passEAST(image,detector):
    (h, w) = image.shape[:2]
    # make a blob from image and forward pass it to EAST
    blob = cv2.dnn.blobFromImage(image, 1.0, (w,h), 
        (123.68, 116.78, 103.94), swapRB=True, crop=False)


    detector.network.setInput(blob) # toss blob to network
    (scores, geometry) = detector.network.forward(detector.layers) # network output

    # calculate bounding box and probability score for each text
    (r, c) = scores.shape[2:4]
    rectangles = [] # init bound box coords for each text region
    confidence = [] # init confidence for text region, parallel with rectangles

    # compute boundary boxes
    phi = 0.33 # bounding box expansion factor
    for y in range(0,r):
        scoreData = scores[0,0,y]
        x0 = geometry[0,0,y] 
        x1 = geometry[0,1,y]
        x2 = geometry[0,2,y]
        x3 = geometry[0,3,y]
        angle = geometry[0,4,y]

        for x in range(0,c):
            if scoreData[x] < detector.confidence:
                continue

            xEnd = 4.0*x + (x1[x]*numpy.cos(angle[x])) + (x2[x]*numpy.sin(angle[x]))
            yEnd = 4.0*y - (x1[x]*numpy.sin(angle[x])) + (x2[x]*numpy.cos(angle[x]))
            xStart = xEnd - x1[x] - x3[x]
            yStart = yEnd - x0[x] - x2[x]
            width = xEnd - xStart
            height = yEnd - yStart

            # expand bound boxes, make sure don't overpass image boundaries
            xEnd = min((xEnd + phi*width),960)
            yEnd = min((yEnd + phi*height),512)
            xStart = max((xStart - phi*width),0)
            yStart = max((yStart - phi*height),0)

            # cv2.rectangle(image, (xStart,yStart), (xEnd,yEnd), (0,255,0), 2)
            # cv2.imshow("im",image)
            # cv2.waitKey(0)

            rectangles.append((xStart, yStart, xEnd, yEnd))
            confidence.append(scoreData[x])

    boxes = non_max_suppression(numpy.array(rectangles),probs=confidence,overlapThresh=0.05)
    
    return boxes

def postEAST(frame,boxes):
    for(xStart, yStart, xEnd, yEnd) in boxes:
        cv2.rectangle(frame, (xStart,yStart), (xEnd,yEnd), (0,255,0), 2)
    
    return frame

def ocr(frame, boxes, config):
    
    solution = []

    for (xStart, yStart, xEnd, yEnd) in boxes:
        snippet = frame[yStart:yEnd, xStart:xEnd]
        # cv2.imshow("yes",snippet)
        # cv2.waitKey(0)
        # snippet = cv2.cvtColor(snippet, cv2.COLOR_BGR2GRAY)
        # snippet = cv2.threshold(snippet,0, 255,
        #     cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # # snippet = cv2.medianBlur(snippet,3)
        # snippet = cv2.cvtColor(snippet, cv2.COLOR_GRAY2BGR)

        cv2.imshow("yes",snippet)
        cv2.waitKey(0)

        text = pytesseract.image_to_string(snippet, config=config, timeout=3)

        solution.append(((xStart, yStart, xEnd, yEnd), text))

    return solution