import numpy as np
import math as m 

def random2Ddepth(width,scaling_factor):
    "Gives random depth list from 0 to 100, divided by scaling factor"

    import random as r

    depth = []
    for _i in range(width):
        dist = r.randrange(1,100) / scaling_factor
        depth.append(int(dist))
        
    return depth
def random_coords(size_range):
    "Gives random coordiantes (xbottomleft, ybottomleft, xtopright, ytopright) for the object box within frame size >~10"

    import random as r

    xtopright = r.randrange(1,size_range - 10) + 10
    xbottomleft = r.randrange(1,xtopright - 8)
    ybottomleft = r.randrange(1,size_range - 10) + 10
    ytopright = r.randrange(1,ybottomleft - 8)

    coords = [xbottomleft, ybottomleft, xtopright, ytopright]
    return coords

#INITILATION
FOV = 90 *m.pi/180 #90 degree horizontal field of view in radians
w_frame  = 200 #pixel width of frame
dt = 0.1 #seconds between frames for 10 frames/s 

#IMPORTING DATA
depth2 = random2Ddepth(w_frame,1) #current frame depth
depth1 = random2Ddepth(w_frame,1) #previous frame depth
coords2 = random_coords(w_frame) #current frame object box coords
coords1 = random_coords(w_frame) #previous frame object box coord

#CALCULATING OBJECT BOX POSITION IN R AND THETA
theta2 = 0.5*( (2*coords2[0]/w_frame -1) + (2*coords2[2]/w_frame -1) ) * FOV/2
theta1 = 0.5*( (2*coords1[0]/w_frame -1) + (2*coords1[2]/w_frame -1) ) * FOV/2
r2 = np.mean(depth2[coords2[0]-1:coords2[2]-1])
r1 = np.mean(depth1[coords1[0]-1:coords1[2]-1])

#test case:
theta2 = 1.5 *m.pi/180
theta1 = 0 *m.pi/180
r2 = 49.5
r1 = 50

#CALCULATING POLAR v(r,theta) AND CARTESIAN v(x,z) VELOCITIES
v_polar = [round((r2-r1)/dt,2) , round(0.5*(r2+r1)*(theta2-theta1)/dt,2)] #depth units per second, rad/s 
v_cart =  [round((r2*m.sin(theta2)-r1*m.sin(theta1))/dt,2),round((r2*m.cos(theta2)-r1*m.cos(theta1))/dt,2)]

#OUTPUT
print("\nObject angle changed from "+ str(round(theta1*180/m.pi,3)) + " to " +str(round(theta2*180/m.pi,3)) +" degrees in "+ str(dt)+" seconds")
print("Object depth changed from "+ str(round(r1,2)) + " to " +str(round(r2,2)) +" units in "+ str(dt)+" seconds")

print("Polar velocity v(r,theta) = " +str(v_polar)+ "  (unit/s, rad/s)")
print("Cartesian velocity v(x,z) = " +str(v_cart)+ "  (unit/s)")