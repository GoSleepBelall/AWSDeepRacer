# This Reward Function is for Track re:Invent 2018
# The function focus on the position of DeepRacer on the track (when to stay on left side and vice versa)
# The function also focuses on the high speed positions in the track when the track path is STRAIGHT
"""
# Difference:
1. Added Track Direction Optimization when the track is optimized
2. Added Additional Rewards
"""
import math
def reward_function(params):
    ################## INPUT PARAMETERS ###################
    # Read input parameters
    distance_from_center = params['distance_from_center']
    is_offtrack = params['is_offtrack']
    x = params['x']
    y = params['y']
    is_left_of_center = params['is_left_of_center']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    steps = params['steps']
    progress = params['progress']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    marker = 0.1 * track_width

    # set threshold
    SPEED_THRESHOLD_1 = 1.8
    SPEED_THRESHOLD_2 = 1.3
    DIRECTION_THRESHOLD = 3.0

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    benchmark_time = 12.0
    benchmark_steps = 173

    center = [25, 26, 52, 59]

    off = [29, 30, 31, 32, 33, 34]
    # This (R) represents the waypoints where DeepRacer should be on right of track
    R = [5, 6, 7, 8, 9,
         26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
         53, 54, 55, 56, 57, 58]

    # This (L) represents the waypoints where DeepRacer should be on left of track
    L = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
         60, 61, 62, 63, 64, 65, 66, 67]

    # This (high_speed) represents the waypoints where DeepRacer should be focusing on speed only
    high_speed = [68, 69, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                  25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 52, 53, 54, 55, 56, 57, 58, 59, 60]
    # Initialise reward
    reward = 1.0

    # Get reward if completes the lap and more reward if it is faster than benchmark_time
    if progress == 100:
        if round(steps / 15, 1) < benchmark_time:
            reward += 100 * round(steps / 15, 1) / benchmark_time
        else:
            reward += 100
    elif is_offtrack:
        reward -= 50

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Speed Optimization
    if (closest_waypoints[0] in (high_speed)) and (speed > 3):
        reward += 150

    # Track Optimization 1
    if (closest_waypoints[1] in (off)) and not all_wheels_on_track:
        reward += 100
    elif (closest_waypoints[0] in (center)) and distance_from_center <= marker:
        reward += 150

    # Track Optimization 2
    if (closest_waypoints[0] in (L)) and (is_left_of_center == True):
        reward += 150
    elif (closest_waypoints[0] in (R)) and (is_left_of_center == False):
        reward += 150
    else:
        reward -= 10

    # If the track is curvy, The direction should be according to track
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)
    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    # Penalize the reward if the difference is too large
    direction_bonus = 1
    if direction_diff > DIRECTION_THRESHOLD or not all_wheels_on_track:
        reward -= 50
    else:
        reward -= 50

    if direction_diff < DIRECTION_THRESHOLD and speed > 2:
        reward += 100

    # Additional Rewards
    # Give additional reward if all wheels are on track
    # Reward for staying on track
    if all_wheels_on_track and distance_from_center <= 0.5 * track_width:
        reward += 100

    # Give additional reward if the car pass every 50 steps faster than expected
    if (steps % 50) == 0 and progress >= (steps / benchmark_steps) * 100:
        reward += 50
    # Penalize if the car cannot finish the track in less than benchmark_steps
    elif (steps % 50) == 0 and progress < (steps / benchmark_steps) * 100:
        reward -= 35

    # Penalize the car for taking too much time to complete a lap
    if steps > 10 and progress / steps < 1:
        reward -= 1
    else:
        reward += 20

    return float(reward)
