"""
Trajectory Planning using Rapidly-Exploring Random Trees (RRT)

Purdue University, West Lafayette, IN
School of Engineering, Aeronautical and Astronautical Engineering, AAE 497 
Computer Vision
"""

# Import modules
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


class RRT:
    """
    Class for RRT algorithm path planning
    """

    class Node:
        """
        Class for RRT Node assignment
        """

        def __init__(self, x, y):
            """
            Parameter types
            :type x: float
            :type y: float
            """
            self.x = x
            self.y = y
            self.x_path = []
            self.y_path = []
            self.parent = None

    def __init__(self, start, goal, obstacles, xy_field, extend_dist, velocity,
                 max_angle, iterations):
        """
        Setting Parameters
        :param start: Starting position of simulation [x,y]
        :param goal: Goal position of the simulation  [x,y]
        :param obstacles: List of obstacles [[x,y,radius],...]
        :param xy_field: The field size of simulation [min,max]
        :param extend_dist: Distance to extend for each step
        :param velocity: Velocity of maneuvering
        :param max_angle: Angle limit that the vehicle can turn
        :param iterations: Iterations for the simulation
        """

        self.start = self.Node(start[0], start[1])
        self.goal = self.Node(goal[0], goal[1])
        self.obstacles = obstacles
        self.field_lower_limit = min(xy_field)
        self.field_upper_limit = max(xy_field)
        self.extend_dist = extend_dist
        self.velocity = velocity
        self.max_angle = max_angle
        self.iterations = iterations
        self.theta1 = 0  # Angle between child and grandparent
        self.theta2 = None  # Angle between child and parent
        self.nodes = []  # List of all nodes to be stored

    def path_planning(self, show_animation=True):
        """
        RRT path planning function.
        :param show_animation: Boolean to choose whether to show animation
        :return: Finalized optimal path
        """

        self.nodes = [self.start]  # Store the starting point in the node list
        for i in range(self.iterations):
            rand_node = self.generate_random_node(i)
            closest_node_index = self.get_closest_node_index(self.nodes, rand_node)
            closest_node = self.nodes[closest_node_index]  # Find the closest node

            next_node = self.maneuver(closest_node, rand_node, self.extend_dist)

            # Check constraints
            # Collision and angle
            if self.obstacle_check(next_node, self.obstacles) or self.angle_check(next_node):
                self.nodes.append(next_node)

            # Plot Simulation
            if show_animation and i % 50 == 0:
                self.plot_simulation(rand_node)

            # Approaching goal
            dist2goal, _ = self.calc_distance_and_angle(self.nodes[-1], self.goal)
            if dist2goal <= self.extend_dist:
                last_node = self.maneuver(self.nodes[-1], self.goal, self.extend_dist)
                # Final check for obstacles
                if self.obstacle_check(last_node, self.obstacles):
                    return self.optimal_path()

        return None  # Impossible to find path

    def generate_random_node(self, iteration_count):
        """
        Function to generation random node
        :param iteration_count: The current iteration count of path planning
        :return: The generated random node
        """
        if iteration_count < self.iterations / random.uniform(1.5, 2):
            # Allow the iteration to continue for some certain amount
            rand1 = random.uniform(self.field_lower_limit, self.field_upper_limit)
            rand2 = random.uniform(self.field_lower_limit, self.field_upper_limit)
            rand_node = self.Node(rand1, rand2)  # Generate random node
        else:
            rand_nums = np.random.randint(0, 100, 2)
            if rand_nums[0] == rand_nums[1]:
                rand1 = random.uniform(self.field_lower_limit, self.field_upper_limit)
                rand2 = random.uniform(self.field_lower_limit, self.field_upper_limit)
                rand_node = self.Node(rand1, rand2)
            else:  # Goal point sampling
                rand_node = self.Node(self.goal.x, self.goal.y)
        return rand_node

    def maneuver(self, node1, node2, extend_dist):
        """
        Function to maneuver to the new node
        :param node1: The departing node
        :param node2: The arriving node
        :param extend_dist: The limit of distance we can move
        :return: the destination/next node
        """

        next_node = self.Node(node1.x, node1.y)  # Preallocate the destination as an object of departing node
        dist, self.theta2 = self.calc_distance_and_angle(next_node, node2)  # Obtain the distance and angle

        # Add the node to the path of the temporary next node
        next_node.x_path = [next_node.x]
        next_node.y_path = [next_node.y]

        # Adjust the extending distance if it is longer than the distance of the nodes
        if extend_dist > dist:
            extend_dist = dist

        time = math.floor(extend_dist / self.velocity)

        for _ in range(time):
            next_node.x += self.velocity * math.cos(self.theta2)
            next_node.y += self.velocity * math.sin(self.theta2)
            next_node.x_path.append(next_node.x)
            next_node.y_path.append(next_node.y)

        dist, self.theta2 = self.calc_distance_and_angle(next_node, node2)  # Recalculate the distance
        if dist <= self.velocity:
            next_node.x_path.append(node2.x)
            next_node.y_path.append(node2.y)

        next_node.parent = node1  # Set the departing node as parent

        return next_node

    def angle_check(self, node):
        """
        Function to check if the angle satisfies conditions
        :param node: The arriving node
        :return: Boolean of True/False of whether the condition is satisfied
        """

        if node is None:  # Check if node is empty
            return False

        closest_node2node_parent_idx = self.get_closest_node_index(self.nodes, node.parent)
        closes_node2node_parent = self.nodes[closest_node2node_parent_idx]
        _, self.theta1 = self.calc_distance_and_angle(closes_node2node_parent, node.parent)
        if self.theta2 - self.theta1 > self.max_angle:
            return False  # Not satisfied

        return False  # Satisfied

    def plot_simulation(self, rand_node=None):
        """
        Function to plot the simulation
        :param rand_node: The generated random node
        :param ax: The axes flag of the figure
        :return: None
        """
        plt.clf()  # Clear all figures

        plt.plot(self.start.x, self.start.y, 'xr')  # Plotting starting point
        plt.plot(self.goal.x, self.goal.y, 'xr')  # Plotting the destination

        if rand_node is not None:  # Plotting the current random node
            plt.plot(rand_node.x, rand_node.y, "hk")

        for node in self.nodes:  # Plotting all the possible paths
            if node.parent:
                plt.plot(node.x_path, node.y_path, '-c')

        fig = plt.gcf()
        ax = fig.gca()
        for (x_center, y_center, radius) in self.obstacles:
            circle = plt.Circle((x_center, y_center), radius, color='k')
            ax.add_patch(circle)

        custom_lines = [Line2D([0], [0], color='r', lw=2)]
        plt.legend(custom_lines, ['Optimal Path'], loc="upper left")
        plt.title("Rapidly-Exploring Random Tree")

        plt.axis("equal")
        plt.axis([self.field_lower_limit, self.field_upper_limit,
                  self.field_lower_limit, self.field_upper_limit])
        plt.grid(True)
        plt.pause(0.01)

    def optimal_path(self):
        """
        Function that computes the optimal path
        :param last_idx: The goal index of the node list
        :return: The optimal path
        """

        opt_path = [[self.goal.x, self.goal.y]]
        node = self.nodes[-1]
        while node.parent is not None:
            opt_path.append([node.x, node.y])
            node = node.parent  # March up the tree until parent becomes None
        opt_path.append([node.x, node.y])  # Append the last remaining value

        return opt_path


    @staticmethod
    def get_closest_node_index(nodes, rand_node):
        """
        Function to calculate the closest node to the randomly generated node
        :param nodes: All of the possible nodes
        :param rand_node: The randomly generated node we are heading to
        :return: The index of the closest node
        """

        distances = [(node.x - rand_node.x) ** 2 + (node.y - rand_node.y) ** 2 for node in nodes]
        idx = distances.index(min(distances))
        return idx

    @staticmethod
    def calc_distance_and_angle(node1, node2):
        """
        Function to calculate the distance and angle from the departing node and arriving node
        :param node1: Departing node
        :param node2: Arriving node
        :return: Distance and angle
        """
        dx = node2.x - node1.x
        dy = node2.y - node1.y
        dist = math.hypot(dx, dy)
        theta = math.atan2(dy, dx)
        return dist, theta

    @staticmethod
    def obstacle_check(node, obstacles):
        """
        Function to check if the arriving node collides with any obstacles
        :param node: The arriving node
        :param obstacles: The list of obstacles
        :return: Boolean of True/False of whether there is no collision
        """
        if node is None:  # Check if the node is empty
            return False

        for (x_center, y_center, radius) in obstacles:
            x_distances = [x_center - x for x in node.x_path]
            y_distances = [y_center - y for y in node.y_path]
            distances = [math.sqrt(dx ** 2 + dy ** 2) for (dx, dy) in zip(x_distances, y_distances)]
            if min(distances) <= radius:
                return False  # Collides with obstacle

        return True  # Clear