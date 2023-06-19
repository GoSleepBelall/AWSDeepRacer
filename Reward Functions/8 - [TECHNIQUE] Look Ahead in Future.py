# This is not a optimal (complete) reward function
# It is just an explanation of implementation of a technique
# Using this technique you can get a dynamic optimal path for future steps
import math

# Description
""" The function is used to create a line between two points in x-y coordinates,
    the points of line will be separated by the difference of distance parameter."""

# Parameters:
# x1: x coordinate of starting point
# y1: y coordinate of starting point
# x2: x coordinate of ending point
# y2: y coordinate of ending point
# distance: distance between points of lines

def get_line_points(x1, y1, x2, y2, distance=0.1):
    dx = x2 - x1
    dy = y2 - y1
    line_length = math.sqrt(dx ** 2 + dy ** 2)
    num_points = int(line_length / distance) + 1
    x_steps = dx / (num_points - 1)
    y_steps = dy / (num_points - 1)
    line_points = [(x1 + i * x_steps, y1 + i * y_steps) for i in range(num_points)]
    return line_points


# Description:
""" This function takes the current waypoint and find the next three waypoints."""

# Parameters:
# params: The dictionary of AWS from AWS

def find_next_three_waypoints(params):
    waypoints = params['waypoints']
    next_points = (list(range(params['closest_waypoint'][1], params['closest_waypoint'][1] + 3)))
    for i in range(len(next_points)):
        if next_points[i] > len(waypoints):
            next_points[i] -= len(waypoints)
    return next_points


def reward_function(params):
    # Get all waypoints
    waypoints = params['waypoints']
    reward = 1
    # Get current position
    x = params['x']
    y = params['y']

    next_points = find_next_three_waypoints(params)

    # Get Destination coordinates
    x_forward = waypoints[next_points[2]][0]
    y_forward = waypoints[next_points[2]][1]

    optimal_path = get_line_points(x, y, x_forward, y_forward)

    # ... perform your operations
    return reward
