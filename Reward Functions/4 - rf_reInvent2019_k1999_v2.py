# This reward function is for track re:Invent 2018
# This reward function focuses on K199 track
"""
Differences:
1- Changed the whole technique and focused on optimal path line of k1999 algorithm.
2- Introduced Speed Threshold for maximize reward at good speeds
"""
import math



def reward_function(params):
    ################## INPUT PARAMETERS ###################
    # Read input parameters
    is_offtrack = params['is_offtrack']
    x = params['x']
    y = params['y']
    speed = params['speed']
    steps = params['steps']
    progress = params['progress']
    track_width = params['track_width']
    steering_angle = params['steering_angle']
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
    x_down = [2.8873885499889385, 3.1675912209711705, 3.4551731738475713, 3.7532515756822287, 4.072814338243193,
              4.500002230529587, 4.549995073956144, 5.117381147897781, 5.447982562982464, 5.711265580422473,
              5.941372105449603, 6.14912709690292, 6.336758932063642, 6.503516690922521, 6.647625884029711,
              6.767148492564518, 1.4547258930465157, 1.5865309544578126, 1.7447260773737912, 1.9265552947643938,
              2.1328222834811292, 2.3641125208150084, 2.617512764005648, 2.8873885499889385]
    y_down = [0.726467741007691, 0.704786488311369, 0.6921786257120108, 0.6858100463187193, 0.6836081931173711,
              0.6837609167129147, 0.6837787896136626, 0.6908041075226552, 0.7112322029646044, 0.7422346953355425,
              0.7849646168697144, 0.8407803487746184, 0.910667356962588, 0.9948399398813299, 1.0933636666158342,
              1.2064015782188044, 1.2610931996668353, 1.1364118322222136, 1.0322868812760757, 0.9430548066740163,
              0.8677942536468937, 0.8067988687678815, 0.759921447767141, 0.726467741007691]

    # set threshold
    SPEED_THRESHOLD_1 = 3
    SPEED_THRESHOLD_2 = 2
    SPEED_THRESHOLD_3 = 1.5
    SPEED_THRESHOLD_4 = 1.3
    DISTANCE_THRESHOLD1 = 0.05 * track_width
    DISTANCE_THRESHOLD2 = 0.1 * track_width

    DIRECTION_THRESHOLD1 = 3.0
    DIRECTION_THRESHOLD2 = 5.0

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


    # Additional Reward for exact optimal line of k1999 (rare)
    if x in (X) and y in (Y):
        reward += 200
    if speed >= SPEED_THRESHOLD_1:
        reward += 200
    elif speed >= SPEED_THRESHOLD_2:
        reward += 150
    elif speed >= SPEED_THRESHOLD_3:
        reward += 100
    elif speed >= SPEED_THRESHOLD_4:
        reward += 50

    if (x in (x_down) and y in (y_down)) and speed >= SPEED_THRESHOLD_1:
        reward += 200
    if (x in (x_down) and y in (y_down)) and speed >= SPEED_THRESHOLD_2:
        reward += 100


    agent_pos = (x,y)
    # Find the nearest point on the track line to the agent
    min_dist = math.inf
    nearest_point = None
    for x, y in zip(X, Y):
        dist = math.sqrt((x - agent_pos[0]) ** 2 + (y - agent_pos[1]) ** 2)
        if dist < min_dist:
            min_dist = dist
            nearest_point = (x, y)

    # Reward the agent if it moves towards the nearest optimal point
    if agent_pos != nearest_point:
        new_dist = math.sqrt((nearest_point[0] - agent_pos[0]) ** 2 + (nearest_point[1] - agent_pos[1]) ** 2)
        if new_dist < DISTANCE_THRESHOLD1:
            reward += 200
            if speed >= SPEED_THRESHOLD_1:
                reward += 200
            elif speed >= SPEED_THRESHOLD_2:
                reward += 150
            elif speed >= SPEED_THRESHOLD_3:
                reward += 100
            elif speed >= SPEED_THRESHOLD_4:
                reward += 50
        elif new_dist < DISTANCE_THRESHOLD2:
            reward += 100
            if speed >= SPEED_THRESHOLD_1:
                reward += 100
            elif speed >= SPEED_THRESHOLD_2:
                reward += 75
            elif speed >= SPEED_THRESHOLD_3:
                reward += 50
            elif speed >= SPEED_THRESHOLD_4:
                reward += 25

    # Calculate the steering angle from the agent's current position to the nearest point
    dx = nearest_point[0] - agent_pos[0]
    dy = nearest_point[1] - agent_pos[1]
    required_steering_angle = math.atan2(dy, dx)

    # The steering angle is in radians, so you may need to convert it to degrees
    required_steering_angle = math.degrees(required_steering_angle)
    if abs(steering_angle - required_steering_angle) < DIRECTION_THRESHOLD1:
        reward += 200
    elif abs(steering_angle - required_steering_angle) < DIRECTION_THRESHOLD2:
        reward += 100


    # Give additional reward if the car pass every 50 steps faster than expected
    if (steps % 50) == 0 and progress >= (steps / benchmark_steps) * 100:
        reward += 200

    return float(reward)
