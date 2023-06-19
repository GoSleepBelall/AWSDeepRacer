


# This is not a optimal (complete) reward function
# It is just an explanation of implementation of a technique
# Using this technique you can get a dynamic optimal path for future steps
import math

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

    # Calculate reward for alignment with optimal steering direction
    heading = params['heading']
    optimal_heading = math.degrees(math.atan2(y_forward - y, x_forward - x))
    heading_diff = abs(optimal_heading - heading)
    if heading_diff > 180:
        heading_diff = 360 - heading_diff
    reward_alignment = math.cos(math.radians(heading_diff))

    # This is one kind of reward, you can integrate this with some other techniques to make your optimal reward
    return reward
