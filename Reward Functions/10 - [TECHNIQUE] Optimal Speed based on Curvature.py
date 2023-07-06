import math

def angle_between_points(first_point, x, third_point):
    """Calculates the angle between two line segments formed by three points."""
    first_dx = first_point[0] - x
    first_dy = first_point[1] - 0
    third_dx = third_point[0] - x
    third_dy = third_point[1] - 0
    angle = math.atan2(third_dy, third_dx) - math.atan2(first_dy, first_dx)
    return math.degrees(angle)


def reward_function(params):
    # ... previous functionality
    # Calculate curvature
    first_point = waypoints[next_points[0]]
    third_point = waypoints[next_points[2]]
    curvature = angle_between_points(first_point, x, third_point)

    # Optimal speed based on curvature
    min_speed, max_speed = 1, 4
    # Changed to continuous function for optimal speed calculation
    optimal_speed = max_speed - (curvature / 180) * (max_speed - min_speed)

    # Calculate reward for speed
    speed_diff = abs(params['speed'] - optimal_speed)
    reward_speed = math.exp(-0.5 * speed_diff)

    # ... Next functionalities
    # ... return weighted reward