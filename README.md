# AWSDeepRacer
Some of my reward functions that helped me throughout my learning.

Being an undergrad student, I'm learning Reinforcement learning and getting hands on experience with AWS Deepracer.
I dont guarantee any reward function will work optimal, This repository is just a representation of my research and learning journey.

# Easiest Log Analysis
## For Begineers
In the learning journey of AWS DeepRacer, i felt need of Log analysis of my model to see what track it is opting and where it is lacking behind by drawing some comparisons in between all episodes as shown below:

![route taken by DeepRacer](https://github.com/GoSleepBelall/AWSDeepRacer/blob/ae29f404bcd2e24880254cb5089091a9c082b015/Log%20Analysis/track_followed.png)

If you want to analyze your routes similarly:
- just download LOG files from AWS DeepRacer
- copy path of: ```logs > training > *-robomaker.log``` file and paste it in code
- define number of episodes
- run
