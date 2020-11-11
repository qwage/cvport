### PACKAGE IMPORT ###
import serial
import time
from numpy import *


### OPEN USB PORT ###
gps = serial.Serial("/dev/ttyACM0", baudrate=9600)


### INITIALIZATIONS ###
ST = time.time()#Start time
lat_x = []
lon_y = []


### READ DATA ### 
while (time.time() - ST) <= 15:
#while True:
    
    line = gps.readline()
    data = line.decode('utf-8')
    data = data.split(",")
    
    if data[0] == "$GPGGA"
        satNum = data[5] #Number of satellites being tracked
        
    if data[0] == "$GPRMC": #Look for GPRMC data only
        if data[2] == "A": #Check satilites are active
            
            cLat = data[3] #Current Latitude
            cLon = data[5] #Current Longitude
            
            '''
            print("\nTime: ",data[1],"UTC")
            print("Lat: ", data[3])
            print("Lon: ", data[5])
            print("Speed: ",data[7], "Knots")
            '''
            
            lat_x.append(data[3]) #Latitude vector construction
            lon_y.append(data[5]) #Longitude vector construction
            
        else:
            print("Void")

