# Importing modules
from rrt_model import RRT
from spline_traj import BSplineSmooth
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)

class DYNRRT:
    # dynamic rrt model 

    def __init__(self, obstacle_info, rrt_extension, rrt_vel, start, goal, 
                    prediction_time, field):
        self.obstacle_pos = obstacle_info[:, 0:2]
        self.obstacle_vel = obstacle_info[:, 2:]
        self.rrt_extension = rrt_extension
        self.rrt_vel = rrt_vel
        self.obstacle_final_pos = None
        self.prediction_time = prediction_time
        self.line_info = np.asarray([[]], dtype=float)
        self.start = start
        self.goal = goal
        self.field = field
        self.opt_path = None
        self.x_smooth = None
        self.y_smooth = None
        self.obstacles = None
        self.flag = True

    def generate_path(self):
        self.predict_obstacle_path()

        if self.check_intersection():
            dyn_obstacles = self.gen_obstacle_line()
            self.obstacles = dyn_obstacles
            # run rrt
            rrt = RRT(start=self.start, goal=self.goal, obstacles=dyn_obstacles, xy_field=self.field,
                        extend_dist=self.rrt_extension, velocity=self.rrt_vel, iterations=100)
            
            opt_path = rrt.path_planning(show_animation=True)
            self.opt_path = opt_path[::-1]
            path_clear = False
            self.flag = path_clear
            return opt_path[::-1], path_clear
        else: 
            opt_path = np.concatenate(([self.start], [self.goal]), axis=0)
            self.opt_path = opt_path
            path_clear = True
            self.flag = path_clear
            return opt_path, path_clear
        return

    def smooth_path(self):
        x_opt_path = [x for (x, y) in self.opt_path]  # Extracting x values
        y_opt_path = [y for (x, y) in self.opt_path]  # Extracting y values
        bsps = BSplineSmooth(x_opt_path, y_opt_path, kval=2, sval=10, point_interval=0.01)
        x_smooth_path, y_smooth_path = bsps.spline_traj()
        self.x_smooth, self.y_smooth = x_smooth_path, y_smooth_path
        return x_smooth_path, y_smooth_path

    def predict_obstacle_path(self):
        new_node = self.obstacle_pos + self.obstacle_vel * self.prediction_time
        self.obstacle_final_pos = new_node
        return 


    # def get_lines(self, points):
    #     slope, y_insct, xmax, xmin = [], [], [], []
    #     for i in range(points.shape[0] - 1):
    #         m_temp, b_temp = self.get_line_coeffs(points[i], points[i + 1])
    #         slope.append(m_temp)
    #         y_insct.append(b_temp)
    #         xmax.append(max(points[i, 0], points[i + 1, 0]))
    #         xmin.append(min(points[i, 0], points[i + 1, 0]))
    #     return slope, y_insct, xmax, xmin

    def get_line(self, point1, point2):
        slope, y_insct = self.get_line_coeffs(point1, point2)
        xmax = max(point1[0], point2[0])
        xmin = min(point1[0], point2[0])
        d = math.hypot(point1[0]-point2[0], point1[1]-point2[1])
        return slope, y_insct, xmax, xmin, d

    def make_lines(self):
        lines = []
        for pt1, pt2 in zip(self.obstacle_pos, self.obstacle_final_pos):
            slope, y_intersect, xmax, xmin, d = self.get_line(pt1, pt2)
            lines.append([slope, y_intersect, xmax, xmin, d])
        self.line_info = lines
        return

    def plot_trajectory(self):
        fig, ax = plt.subplots()
        plt.scatter(self.start[0], self.start[1], c='b')
        x_opt_path = [x for (x, y) in self.opt_path]  # Extracting x values
        y_opt_path = [y for (x, y) in self.opt_path]  # Extracting y values
        plt.plot(x_opt_path, y_opt_path, c='k')
        plt.scatter(self.goal[0], self.goal[1], c='r')

        if not self.flag:
            plt.plot(self.x_smooth, self.y_smooth, c='b')
            for (x_center, y_center, radius) in self.obstacles:
                circle = plt.Circle((x_center, y_center), radius, color='k')
                ax.add_patch(circle)
        else:
            for (pt1, pt2) in zip(self.obstacle_pos, self.obstacle_final_pos):
                plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], '-g')

        plt.grid(which='both', axis='both', linestyle=':')
        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.xaxis.set_minor_locator(MultipleLocator(5))
        plt.show()

    @staticmethod
    def get_line_coeffs(p1, p2):
        if np.all(p1 == 0):
            m = p2[1] / p2[0]
            b = 0
        elif np.all(p2 == 0):
            m = p1[1] / p1[0]
            b = 0
        else:
            m = (p2[1] - p1[1]) / (p2[0] - p1[0])
            b = p1[1] - m * p1[0]
        return m, b

    def gen_obstacle_line(self):
        self.make_lines()
        obstacles = []
        for m, b, xmax, xmin, d in self.line_info:
            for xcenter in np.linspace(xmin, xmax, math.ceil(d**3)):
                circle = (xcenter, m * xcenter + b, 1)
                obstacles.append(circle)
        # temp = np.array(obstacles)
        # obst_dist = cdist([self.nodes[-1]], temp[:, :2], 'euclidean')
        # idx = np.where(obst_dist <= 1.5)
        # obstacles = np.delete(temp, idx, axis=0)
        return obstacles

    
    @staticmethod
    def calc_intersect(p1: list, p2: list, p3: list, p4: list):
        """
        Function that computes the [x, y] of the intersection of 2 lines using the 4 points [x, y]
        """
        x1, x2, x3, x4 = p1[0], p2[0], p3[0], p4[0]
        y1, y2, y3, y4 = p1[1], p2[1], p3[1], p4[1]
        # xy-position of intersection
        Px = (((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) /
              ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)))
        Py = (((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) /
              ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)))
        return np.asarray([Px, Py], dtype=float)

    def check_intersection(self):
        """
        Function that checks if there are any intersections
        """

        n1, n2 = self.start, self.goal
        for n3, n4 in zip(self.obstacle_pos, self.obstacle_final_pos):
            # Compute the intersection for these 4 points
            intersect = self.calc_intersect(n1, n2, n3, n4)

            # Check if this intersection is within the segment of the 4 points
            cond1 = (min(n1[0], n2[0]) <= intersect[0] <= max(n1[0], n2[0])
                     and min(n1[1], n2[1]) <= intersect[1] <= max(n1[1], n2[1]))
            cond2 = (min(n3[0], n4[0]) <= intersect[0] <= max(n3[0], n4[0])
                     and min(n3[1], n4[1]) <= intersect[1] <= max(n3[1], n4[1]))
            if cond1 and cond2:
                return True  # There is an intersection
        return False  # There are no intersections


# Generate random obstacle array
sz = 4
positions = np.random.uniform(-25, 25, (sz, 2))
velocities = np.random.uniform(0.5, 2.0, (sz, 2))
obstacle_array = np.concatenate((positions, velocities), axis=1)

# Initialize the dynamic rrt class 
dynamic_rrt = DYNRRT(obstacle_info=obstacle_array, rrt_extension=15, rrt_vel=8, 
                        start=[-25, 0], goal=[25, 0], prediction_time=4, field=[-50, 50])

print('Check if obstacles is in path. If there is run RRT.')
opt_path, path_clear = dynamic_rrt.generate_path()   # generate optimal path
x_opt_path = [x for (x, y) in opt_path]  # Extracting x values
y_opt_path = [y for (x, y) in opt_path]  # Extracting y values

if not path_clear:
    x_smooth, y_smooth = dynamic_rrt.smooth_path()  # generate smooth path
else:
    print("The path is clear. No path is generated and we go along the desired path.")
dynamic_rrt.plot_trajectory()  # plot trajectory
