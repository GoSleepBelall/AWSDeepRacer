# This Reward Function is for Track re:Invent 2018
# The function focus on the position of DeepRacer on the track (when to stay on left side and vice versa)
# The function also focuses on the high speed positions in the track when the track path is STRAIGHT

def reward_function(params):
    ################## INPUT PARAMETERS ###################
    # Read input parameters
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    is_offtrack = params['is_offtrack']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    steps = params['steps']
    progress = params['progress']
    track_width = params['track_width']
    closest_waypoints = params['closest_waypoints']

    marker = 0.1 * track_width
    benchmark_time = 11.0

    center = [25,26,52,59]
    off = [29,30,31,32,33,34]

    # This (R) represents the waypoints where DeepRacer should be on right of track
    R = [5,6,7,8,9,
         26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,
         53,54,55,56,57,58]

    # This (L) represents the waypoints where DeepRacer should be on left of track
    L = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,
         60,61,62,63,64,65,66,67]

    # This (high_speed) represents the waypoints where DeepRacer should be focusing on speed only
    high_speed = [68,69,0,1,2,3,4,5,6,7,8,9,10,
                  25,26,27,28,29,30,31,32,33,34,35,36,37,38,52,53,54,55,56,57,58,59,60]

    # Initialise reward
    reward = 1.0

    # Reward for completion
    if steps > 0:
        reward += ((progress*150)/steps)**2
    else:
        reward = 1

    # Get reward if completes the lap and more reward if it is faster than benchmark_time
    if progress == 100:
        if round(steps / 15, 1) < benchmark_time:
            reward += 100 * round(steps / 15, 1) / benchmark_time
        else:
            reward += 50
    elif is_offtrack:
        reward -= 50

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

    if is_offtrack:
        reward -= 100

    return float(reward)
