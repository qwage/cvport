import serial
import time
import cv2
import matplotlib.pyplot as plt
from numpy import *
#from sense_hat import SenseHat

gps = serial.Serial("/dev/ttyACM0", baudrate=9600)

#sense = SenseHat()

ST = time.time()
lat_x = []
lon_y = []
while (time.time() - ST) <= 15:
    #sense.show_message("GPS", text_color = [255, 0, 255])
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    line = gps.readline()
    data = line.decode('utf-8')
    data = data.split(",")
    if data[0] == "$GPRMC":
        if data[2] == "A":
            '''
            print("\nTime: ",data[1],"UTC")
            print("Lat: ", data[3])
            print("Lon: ", data[5])
            print("Speed: ",data[7], "Knots")
            '''
            lat_x.append(data[3])
            lon_y.append(data[5])
            
        else:
            print("Void")
    #sense.clear()

currentLat = 4025.29
currentLon = 08654.31002
P5 = .0145
P10 = P5 * 2
P30 = P5 * 6
P1 = P5 / 5
t = arange(0,2*pi,.01)
c5Lat = P5*sin(t) + currentLat
c5Lon = P5*cos(t) + currentLon
c10Lat = P10*sin(t) + currentLat
c10Lon = P10*cos(t) + currentLon
c1Lat = P1*sin(t) + currentLat
c1Lon = P1*cos(t) + currentLon

plt.plot(c5Lat,c5Lon,color="green")
plt.plot(c10Lat,c10Lon,color="red")
plt.plot(c1Lat,c1Lon,color="purple")
plt.plot(double(lat_x),double(lon_y), 'o', color="blue")
plt.xlabel("Latitude")
plt.ylabel("Logitude")
plt.title("Accuracy and Precision of GPS Mouse Unit")
plt.grid(linestyle="--")
plt.legend(("5% Error", "10% Error", "1% Error", "100% Error", "GPS Data"))
plt.axis("equal")
plt.show()