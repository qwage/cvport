import cv2 as cv

# -- Import the Floor Plan of the Airport -- #
floor_plan = cv.imread('Airport Floor Plan.jpg')
gray_img = cv.cvtColor(floor_plan, cv.COLOR_BGR2GRAY)