import re

path = 'C:\\Users\\quinn\\Documents\\Semester 8\\OpenCV Class\\Project\\cvport\\Sample Data\\GPS\\samp_nmea.nmea'
file = open(path)

# initialize list items
zulu = [] #Zulu Time
lat = [] #Latitude
lon = [] #Longitude
sat = [] #Number of satellites being tracked
dilu = [] #Horizontal dilution of position
alt = [] #altitude in meters
hgt = [] #MSL height

count = 0


for line in file:
    chunk = re.split(',+',line)
    zulu.append(chunk[1])
    lat.append(chunk[2])
    lon.append(chunk[4])
    sat.append(chunk[7])
    dilu.append(chunk[8])
    alt.append([9])
    hgt.append([10])


lat_change = float(lat[1]) - float(lat[0]) 
print(lat_change)



