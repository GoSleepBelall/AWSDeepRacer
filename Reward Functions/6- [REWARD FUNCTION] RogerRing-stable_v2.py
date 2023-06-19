# This Steps and Speed Threshold is decided for Roger Ring track, You can change to make it generic
# This is the most Stable model I've ever created, follow the track to it maximum possible effort,
# Try to take stable turns and keeps record of previous step
# More emphasis on Speed
"""
* - (train 120 minutes at v1, then v2 for best result)

Differences:
* - Can be used for generic tracks
* - Optimal for physical environment
1- Totally Different approach (used Object-Oriented Approach)
2- Keeps track of previous step
3- Make Stable Turns
4- Compares speed with previous step speed and get rewards on incriment only if path is straight

Difference from V1:
1- More emphasis on Speed, because v1 was following track very rigidly
"""

import math
class Reward:
    def __init__(self, verbose = False, track_time = False):
        self.prev_speed = 0
    def reward_fun(self, params):
        # Read Parameters
        speed = params['speed']
        waypoints = params['waypoints']
        closest_waypoints = params['closest_waypoints']
        heading = params['heading']
        steps = params['steps']
        progress = params['progress']
        distance_from_center = params['distance_from_center']
        is_offtrack = params['is_offtrack']

        if is_offtrack:
            return 0.0001

        prev_point = waypoints[closest_waypoints[0]]
        next_point = waypoints[closest_waypoints[1]]

        STEPS_THRESHOLD = 300
        DIRECTION_THRESHOLD1 = 3.0
        DIRECTION_THRESHOLD2 = 5.0

        SPEED_THRESHOLD1 = 2.36

        MARKER1 = 0.1*distance_from_center
        MARKER2 = 0.2*distance_from_center

        # Initialize Reward
        reward = 100

        #Check angle
        if heading < 0:
            heading+=360.0

        # Give additional reward if the car pass every 50 steps faster than expected
        if (steps % 50) == 0 and progress >= (steps / STEPS_THRESHOLD) * 100:
            reward += 200

        # If the speed of current step is greater than previous step, give reward
        if (speed > self.prev_speed) and (self.prev_speed > 0):
            reward += 100

        if speed > 3:
            reward += 300
        elif speed > SPEED_THRESHOLD1:
            reward += 200
        elif speed > SPEED_THRESHOLD1 - 0.5:
            reward += 100
        elif speed > SPEED_THRESHOLD1 - 1:
            reward += 50

        # Give reward if heading is in track_direction
        track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
        # Convert to degree
        track_direction = math.degrees(track_direction)
        if track_direction<0:
            track_direction+=360
        # Calculate the difference between the track direction and the heading direction of the car
        direction_diff = abs(track_direction - heading)
        if direction_diff < DIRECTION_THRESHOLD1:
            reward += 100
        elif direction_diff < DIRECTION_THRESHOLD2:
            reward += 50

        abs_track_direction = abs(track_direction)

        # If track is straight (STRONG EMPHASIS ON SPEED AND LOW ZIGZAG)
        if (abs_track_direction >0 and abs_track_direction< 15) or (abs_track_direction > 165 and abs_track_direction < 195) or (abs_track_direction> 345 and abs_track_direction<360):
            if speed > 3:
                reward += 300
            elif speed > SPEED_THRESHOLD1:
                reward += 200
            elif speed > SPEED_THRESHOLD1-0.5:
                reward += 100
            if distance_from_center < MARKER1:
                reward += 100

        self.prev_speed = speed
        return float(reward)


reward_obj = Reward()

def reward_function(params):
    reward = reward_obj.reward_fun(params)
    return float(reward)
