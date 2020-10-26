import cv2
import numpy as np

def mask_image(frame,w,h):
    p1 = (0,h)
    p2 = (int(w/4),0)
    p3 = (int(3*w/4),0)
    p4 = (w,h)
    pts = [p1,p2,p3,p4]
    pts = np.array(pts,dtype='int32')
    mask = np.zeros(frame.shape, np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
    result = cv2.bitwise_and(frame, mask)
    return(result)

cap = cv2.VideoCapture('vid1_Trim.mp4')
scaling_factor = .6
ret1,frame1 = cap.read()
h1,w1,_ = frame1.shape
w1new = int(w1*scaling_factor)
h1new = int(h1*scaling_factor)
frame1 = cv2.resize(frame1,(w1new,h1new))

mask = np.zeros_like(frame1)
it = 0

while cap.isOpened():
    ret2,frame2 = cap.read()

    frame2 = cv2.resize(frame2,(w1new,h1new))
    frame1 = mask_image(frame1,w1new,h1new)
    frame2 = mask_image(frame2,w1new,h1new)
    cv2.imshow('frame1',frame1)
    cv2.imshow('frame2',frame2)
    frame1_gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(frame1_gray,frame2_gray,None,.5,3,15,3,5,1.2,0) #Returns 3D array consisting of each pixel and the corresponding movement (u,v)
    u = flow[...,0]
    v = flow[...,1]
    r,theta = cv2.cartToPolar(u,v)
    mask[...,0] = theta*180/np.pi/2
    mask[...,2] = cv2.normalize(r,None,0,255,cv2.NORM_MINMAX)
    mask = cv2.cvtColor(mask,cv2.COLOR_HSV2BGR)
    
    #blur = cv2.blur(mask,(3,3))
    laplacian = cv2.Laplacian(mask,cv2.CV_64F)
    #erosion = cv2.erode(laplacian,(3,3), iterations = 1)
    
    cv2.imshow('result',laplacian)

    k = cv2.waitKey(20) & 0xff
    if k == 27:
            break
    frame1 = frame2

#Trying to average the results of multiple frames from dense optical flow
"""frames_to_average = 5
frame1 = mask_image(frame1,w1new,h1new)
frame1_gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
Frame = [frame1_gray]
avmask = np.zeros_like(frame1)
while cap.isOpened():
    for num in range(frames_to_average):
        ret2,frame2 = cap.read()
        frame2 = cv2.resize(frame2,(w1new,h1new))
        frame2 = mask_image(frame2,w1new,h1new)
        frame2_gray = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        Frame.append(frame2_gray)
    
    masks = []
    for i in range(frames_to_average):
        flow = cv2.calcOpticalFlowFarneback(Frame[i],Frame[i+1],None,.5,3,15,3,5,1.2,0) #Returns 3D array consisting of each pixel and the corresponding movement (u,v)
        u = flow[...,0]
        v = flow[...,1]
        r,theta = cv2.cartToPolar(u,v)
        mask[...,0] = theta*180/np.pi/2
        mask[...,2] = cv2.normalize(r,None,0,255,cv2.NORM_MINMAX)
        mask = cv2.cvtColor(mask,cv2.COLOR_HSV2BGR)
        masks.append(mask)
    utot = 0
    vtot = 0
    for img in masks:
        u = img[...,0]
        v = img[...,2]
        utot += u
        vtot += v
    uavg = u/len(masks)
    vavg = v/len(masks)
    avmask[...,0] = uavg
    avmask[...,2] = vavg
    gray_img = cv2.cvtColor(avmask,cv2.COLOR_BGR2GRAY)

    blur = cv2.blur(gray_img,(3,3))
    laplacian = cv2.Laplacian(blur,cv2.CV_64F)
    erosion = cv2.erode(laplacian,(3,3), iterations = 1)
    cv2.imshow('maybe',erosion)


    k = cv2.waitKey(20) & 0xff
    if k == 27:
            break
    Frame = [Frame[1]]"""

cv2.destroyAllWindows()
cap.release()

