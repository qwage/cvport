# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# This function imports waypoints from a txt file and plots them  #
#                                                                 #
#                                                                 #
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

import matplotlib.pyplot as plt
import cv2 as cv
import re
from PIL import Image


im = Image.open('maze.png', 'r')
width, height = im.size
pixel_values = list(im.getdata())
print(pixel_values)

'''
path = 'C:\\Users\\quinn\\Documents\\Semester 8\\OpenCV Class\\Project\\cvport\\Sample Data\\GPS\\GPS1.csv'
file = open(path)

lat = []
lon = []

for line in file:
    line = line.strip('\n')
    line = line.split(',')
    lat.append(line[0])
    lon.append(line[1])


plt.plot(lat,lon)
plt.grid()
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.show()
'''