# This reward function is for track re:Invent 2018
# This reward function focuses on K199 track
"""
Differences:
1- Changed the whole technique and focused on optimal path line of k1999 algorithm.
"""
import math

def reward_function(params):
    ################## INPUT PARAMETERS ###################
    # Read input parameters
    distance_from_center = params['distance_from_center']
    is_offtrack = params['is_offtrack']
    x = params['x']
    y = params['y']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    steps = params['steps']
    progress = params['progress']
    steering_angle = params['steering_angle']
    track_width = params['track_width']
    #These X and Y coordinates represent the optimal path as per k1999 algorithm
    X = [2.88738855, 3.16759122, 3.45517317, 3.75325158, 4.07281434, 4.50000223, 4.54999507, 5.11738115, 5.44798256,
         5.71126558, 5.94137211, 6.1491271, 6.33675893, 6.50351669, 6.64762588, 6.76714849, 6.85790417, 6.92193762,
         6.96026824, 6.96689958, 6.92976742, 6.85379617, 6.72693273, 6.56582731, 6.38075512, 6.18037171, 5.97126499,
         5.75829177, 5.55841177, 5.36004947, 5.16333131, 4.96844903, 4.77552032, 4.5846244, 4.39562481, 4.20825035,
         4.02216522, 3.83712807, 3.68186141, 3.52529227, 3.36674073, 3.20532486, 3.0401252, 2.87024421, 2.69486335,
         2.51319321, 2.32452568, 2.12696309, 1.91810508, 1.69471913, 1.45416273, 1.21119005, 1.01922953, 0.92220549,
         0.88926604, 0.89600747, 0.92404943, 0.96605253, 1.01802833, 1.08079017, 1.15513698, 1.24162317, 1.34112998,
         1.45472589, 1.58653095, 1.74472608, 1.92655529, 2.13282228, 2.36411252, 2.61751276, 2.88738855]

    Y = [0.72646774, 0.70478649, 0.69217863, 0.68581005, 0.68360819, 0.68376092, 0.68377879, 0.69080411, 0.7112322,
         0.7422347, 0.78496462, 0.84078035, 0.91066736, 0.99483994, 1.09336367, 1.20640158, 1.33508669, 1.47646609,
         1.62797346, 1.7888072, 1.95515434, 2.11910271, 2.26841633, 2.3979065, 2.50632652, 2.5960265, 2.67207187,
         2.74110301, 2.81013238, 2.88360578, 2.96218803, 3.04682634, 3.13832543, 3.2374528, 3.34419701, 3.45789343,
         3.57740375, 3.70184192, 3.80970389, 3.91179837, 4.00606413, 4.09041474, 4.16335643, 4.22393077, 4.27162279,
         4.30602365, 4.32672382, 4.33080298, 4.31381212, 4.26740868, 4.17400849, 4.00653223, 3.74402202, 3.42050544,
         3.10443889, 2.82076036, 2.56281185, 2.32460305, 2.11228544, 1.91512981, 1.73107571, 1.56014807, 1.40323884,
         1.2610932, 1.13641183, 1.03228688, 0.94305481, 0.86779425, 0.80679887, 0.75992145, 0.72646774]

    # set threshold
    SPEED_THRESHOLD_1 = 1.8
    SPEED_THRESHOLD_2 = 1.3
    DIRECTION_THRESHOLD = 3.0

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    benchmark_time = 8
    benchmark_steps = 120

    straight_waypoints = [0, 1, 2, 3, 4, 5, 6, 7, 8, 29, 30]
    high_speed = [1, 2, 3, 4, 5, 6, 7, 25, 26, 27, 28]

    # Initialise reward
    reward = 1.0

    # Get reward if completes the lap and more reward if it is faster than benchmark_time
    if progress == 100:
        if round(steps / 15, 1) < benchmark_time:
            reward += 100 * round(steps / 15, 1) / benchmark_time
        else:
            reward += 100
    elif is_offtrack:
        reward -= 500
    # Give reward if it follows optimal path line
    if x in (X) and y in (Y):
        reward += 200
    if speed > 3:
        reward += 200

    # Give additional reward if the car pass every 50 steps faster than expected
    if (steps % 50) == 0 and progress >= (steps / benchmark_steps) * 100:
        reward += 50
    # Penalize if the car cannot finish the track in less than benchmark_steps
    elif (steps % 50) == 0 and progress < (steps / benchmark_steps) * 100:
        reward -= 35

    return float(reward)
