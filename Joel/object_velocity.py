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
veh_speed2 = 1 #m/s from  wheels
veh_speed1 = 1 
veh_angle2 = m.pi/2 #rad where pi/2 is north (+y dir.)\
veh_angle1 = m.pi/2

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
theta2 = 0 *m.pi/180
theta1 = 0 *m.pi/180
r2 = 2
r1 = 2.1

#CALCULATING CARTESIAN v(x,y) VELOCITIES
x_2 = r2*m.cos(veh_angle2-theta2)
x_1 = r1*m.cos(veh_angle1-theta1)
y_2 = r2*m.sin(veh_angle2-theta2)
y_1 = r1*m.sin(veh_angle1-theta1)
v_rel =  np.array([(x_2-x_1)/dt,(y_2-y_1)/dt])

v_veh_x = .5*(veh_speed2*m.cos(veh_angle2) + veh_speed1*m.cos(veh_angle1))
v_veh_y = .5*(veh_speed2*m.sin(veh_angle2) + veh_speed1*m.sin(veh_angle1))
v_vehicle = np.array([v_veh_x,v_veh_y])

v_obj_inertial = v_rel + v_vehicle

#OUTPUT
print(v_rel)
print(v_vehicle)
print("Inertial velocity v(x,z) = " +str(v_obj_inertial)+ "  (unit/s)")