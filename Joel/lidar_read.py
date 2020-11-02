import numpy as np
from scipy import interpolate

data_array = np.genfromtxt(r'C:\\Users\\coolm\\OneDrive\\Desktop\\Purdue\\AAE490\\cvport\\Joel\\test01.txt', delimiter=' ')
depth_fcn = interpolate.interp1d(data_array[:,0],data_array[:,1],kind ='nearest',bounds_error=None)

xnew = np.arange(1, 359, 0.1)
print(depth_fcn(xnew))
