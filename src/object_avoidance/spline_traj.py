"""
Smooth RRT generated trajectory using B-Spline 

Purdue University, West Lafayette, IN
School of Engineering, Aeronautical and Astronautical Engineering, AAE 497 
Computer Vision
"""

# Importing necessary modules 
import numpy as np 
from scipy.interpolate import splprep, splev 

class BSplineSmooth:
    """
    Class of the smoothing out a trajectory using the B-Spline method
    """

    def __init__(self, x_points, y_points, kval=1, sval=100, point_interval=0.01):
        """
        Setting parameters
        :param x_points: the x value points generated from a trajectory planning algorithm
        :param y_points: the y value points generated from a trajectory planning algorithm
        :param kval: the degree of spline fit 
        :param sval: the smoothing condition 
        :param point_interval: the percision of the spline 
        """

        self.x_points = np.asarray(x_points, dtype=float)
        self.y_points = np.asarray(y_points, dtype=float)
        self.kval = kval
        self.sval = sval
        self.point_interval = point_interval

        # Reshape the 2 into a column vector 
        # self.x_points = np.reshape(self.x_points, (np.size(self.x_points), 1))
        # self.y_points = np.reshape(self.y_points, (np.size(self.y_points), 1))

    def spline_traj(self):
        """
        Function that conducts the main B-Spline procedure
        """

        # Conduct spline interpolation of the data 
        tck, u = splprep([self.x_points, self.y_points], k=self.kval, s=self.sval)

        # u_new points to project the original points on for the B-Spline
        u_new = np.arange(0, 1.01, self.point_interval)

        # Generate new points 
        x_new, y_new = splev(u_new, tck)

        return x_new, y_new
    

