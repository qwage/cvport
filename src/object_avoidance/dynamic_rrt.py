# Importing modules
from rrt_model import RRT
from spline_traj import BSplineSmooth
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter)
import random


class DYNRRT:
    # dynamic rrt model

    def __init__(self, obstacle_info, rrt_extension, rrt_vel, start, goal, 
                    prediction_time, field, iters):
        self.obstacle_pos = obstacle_info[:, 0:2] 
        self.obstacle_vel = obstacle_info[:, 2:-1]
        self.obstacle_radii = obstacle_info[:, -1]
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
        self.iters = iters
        self.smootherPath = None

    def generate_path(self):
        self.predict_obstacle_path()

        if self.check_intersection():
            dyn_obstacles = self.gen_obstacle_line()
            self.obstacles = dyn_obstacles
            # run rrt
            rrt = RRT(start=self.start, goal=self.goal, obstacles=dyn_obstacles, xy_field=self.field,
                        extend_dist=self.rrt_extension, velocity=self.rrt_vel, iterations=self.iters)
            
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
        smoothJag = SmoothJagged(path_points=self.opt_path, maxIterations=200, 
                                    obstacles=self.obstacles)
        smootherOptPath = smoothJag.byebye_jagged()
        self.smootherPath = smootherOptPath

        x_opt_path = [x for (x, y) in smootherOptPath]  # Extracting x values
        y_opt_path = [y for (x, y) in smootherOptPath]  # Extracting y values

        bsps = BSplineSmooth(x_opt_path, y_opt_path, kval=2, sval=50, point_interval=0.05)
        x_smooth_path, y_smooth_path = bsps.spline_traj()
        self.x_smooth, self.y_smooth = x_smooth_path, y_smooth_path
        return x_smooth_path, y_smooth_path

    def predict_obstacle_path(self):
        new_node = self.obstacle_pos + self.obstacle_vel * self.prediction_time
        self.obstacle_final_pos = new_node
        return 

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
            plt.plot([x for (x, y) in self.smootherPath], [y for (x, y) in self.smootherPath], '--g')
            plt.plot(self.x_smooth, self.y_smooth, c='b')
            for (x_center, y_center, radius) in self.obstacles:
                circle = plt.Circle((x_center, y_center), radius, color='k')
                ax.add_patch(circle)
        else:
            for (pt1, pt2) in zip(self.obstacle_pos, self.obstacle_final_pos):
                plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], '-g')

        plt.grid(which='both', axis='both', linestyle=':')
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(5))
        ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
        ax.yaxis.set_minor_locator(MultipleLocator(1))
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
        i = 0
        for m, b, xmax, xmin, d in self.line_info:
            for xcenter in np.linspace(xmin, xmax, math.ceil(d**2)):
                circle = (xcenter, m * xcenter + b, self.obstacle_radii[i])
                obstacles.append(circle)
            i+=1
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


class SmoothJagged:

    def __init__(self, path_points, maxIterations, obstacles):
        self.path = path_points
        self.maxIter = maxIterations
        self.obstacleList = obstacles

    def get_path_length(self):
        le = 0
        for i in range(len(self.path) - 1):
            dx = self.path[i + 1][0] - self.path[i][0]
            dy = self.path[i + 1][1] - self.path[i][1]
            d = math.sqrt(dx * dx + dy * dy)
            le += d

        return le


    def get_target_point(self, targetL):
        le = 0
        ti = 0
        lastPairLen = 0
        for i in range(len(self.path) - 1):
            dx = self.path[i + 1][0] - self.path[i][0]
            dy = self.path[i + 1][1] - self.path[i][1]
            d = math.sqrt(dx * dx + dy * dy)
            le += d
            if le >= targetL:
                ti = i - 1
                lastPairLen = d
                break

        partRatio = (le - targetL) / lastPairLen

        x = self.path[ti][0] + (self.path[ti + 1][0] - self.path[ti][0]) * partRatio
        y = self.path[ti][1] + (self.path[ti + 1][1] - self.path[ti][1]) * partRatio

        return [x, y, ti]


    def line_collision_check(self, first, second):
        # Line Equation

        x1 = first[0]
        y1 = first[1]
        x2 = second[0]
        y2 = second[1]
        try:
            a = y2 - y1
            b = -(x2 - x1)
            c = y2 * (x2 - x1) - x2 * (y2 - y1)
        except ZeroDivisionError:
            return False

        for (ox, oy, rad) in self.obstacleList:
            d = abs(a * ox + b * oy + c) / (math.sqrt(a * a + b * b))
            if d <= rad:
                return False
        return True  # OK

    def clean_pathpoints(self):
        # Removes redundant points 
        temp_path = np.array(self.path)
        for i in range(temp_path.shape[0]-1):
            point1 = temp_path[i]
            point2 = temp_path[i+1]
            if np.all(point1 - point2 == 0):
                self.path = np.delete(self.path, i, 0)
        return 

    def byebye_jagged(self):
        le = self.get_path_length()
        for i in range(self.maxIter):
            # Sample two points
            pickPoints = [random.uniform(0, le), random.uniform(0, le)]
            pickPoints.sort()
            first = self.get_target_point(pickPoints[0])
            second = self.get_target_point(pickPoints[1])
            if first[2] <= 0 or second[2] <= 0:
                continue
            if (second[2] + 1) > len(self.path):
                continue
            if second[2] == first[2]:
                continue
            # collision check
            if not self.line_collision_check(first, second):
                continue
            # Create New path
            newPath = []
            newPath.extend(self.path[:first[2] + 1])
            newPath.append([first[0], first[1]])
            newPath.append([second[0], second[1]])
            newPath.extend(self.path[second[2] + 1:])
            self.path = newPath
            le = self.get_path_length()
        self.clean_pathpoints()
        return self.path


def clear_obstacle(point, obstacles):
    """
    Function to check if the arriving node collides with any obstacles
    :param point: Random point
    :param obstacles: The list of obstacles
    :return: Boolean of True/False of whether there is no collision
    """

    for (x_center, y_center, _, __, radius) in obstacles:
        x_distance = x_center - point[0]
        y_distance = y_center - point[1]
        distance = math.sqrt(x_distance**2 + y_distance**2)
        if distance <= radius+3:
            return False  # Collides with obstacle
    return True  # Clear

def update_goal(goal_point):
    return goal_point + [3, 0]

# Generate random obstacle array
sz = 10
positions = np.random.uniform(-25, 25, (sz, 2))
velocities = np.random.uniform(-2.0, 2.0, (sz, 2))
radii = np.random.uniform(0.5, 1.5, (sz, 1))
obstacle_array = np.concatenate((positions, velocities, radii), axis=1)

# Update goal point if there is a obstacle or its course on the goal point
end = [25, 0]
while True:
    if not clear_obstacle(end, obstacle_array):
        end = update_goal(end)
    else:
        break

# Initialize the dynamic rrt class 
dynamic_rrt = DYNRRT(obstacle_info=obstacle_array, rrt_extension=10, rrt_vel=3, 
                        start=[-25, 0], goal=end, prediction_time=4, field=[-50, 50], iters=500)

print('Check if obstacles is in path. If there is run RRT.')
opt_path, path_clear = dynamic_rrt.generate_path()   # generate optimal path
x_opt_path = [x for (x, y) in opt_path]  # Extracting x values
y_opt_path = [y for (x, y) in opt_path]  # Extracting y values

if not path_clear:
    x_smooth, y_smooth = dynamic_rrt.smooth_path()  # generate smooth path
else:
    print("The path is clear. No path is generated and we go along the desired path.")
dynamic_rrt.plot_trajectory()  # plot trajectory
