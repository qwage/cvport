import numpy as np
from scipy.spatial import distance as dist

#REQUIRED INPUTS
vehicle_traj = np.array([[1,1.5,2,2.5,3,3.5,4],[2,2,2,2,2,2,2]]) #[x_1 to x_n],[y_1 to y_n]
vehicle_width = 0.8 #meters
object_traj = np.array([[1,1.5,2,2.5,3,3.5,4],[1,1.3,1.6,1.9,2.2,2.5,2.8]]) #meters
object_width = 0.15 #meters 
#note: the changes in distance from each time step assumed to be small compared to width

safety_factor = 1

#DETERMINING ALLOWABLE DISTANCE
allow_dist = 0.5*(vehicle_width + object_width)*safety_factor

#CALCULATING DISTANCES AND CHECKING
traj_dist = []
flag = 0
for i in range(len(object_traj[1,:])):
    distance = dist.euclidean(vehicle_traj[:,i],object_traj[:,i])
    traj_dist.append(distance)
    if distance <= allow_dist:
        flag = 1
        print('Collision detected at time index ' + str(i))

print(traj_dist)
print(allow_dist)