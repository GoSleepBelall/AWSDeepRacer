# Import dependencies
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to filter out lines that only contains log entry
def clear_log(filepath):
    with open(filepath, "r") as infile, open("output.csv", "w") as outfile:
        for line in infile:
            if line.startswith("SIM_TRACE_LOG"):
                outfile.write(line)


# Refine log by adding header into file and removing prefix
def refine_log():
    # Open the input and output files
    with open('output.csv', newline='') as infile, open('log.csv', 'w', newline='') as outfile:
        # Create a CSV reader and writer
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the header row to the output file
        header = ['episode', 'step', 'xc', 'yc', 'heading', 'steering_angle', 'speed',
                  'action_taken', 'reward', 'job_completed', 'all_wheels_on_track', 'progress',
                  'closest_waypoint_index', 'track_length', 'time', 'episode_status']
        writer.writerow(header)

        # Process each row in the input file
        for row in reader:
            # Remove the "SIM_TRACE_LOG" prefix from the first column
            row[0] = row[0].replace('SIM_TRACE_LOG:', '')

            # Convert the action_taken field to a string
            action_taken = '[' + (row[7][1:])+ ',' + (row[8])
            row[7] = action_taken

            # Write the modified row to the output file
            writer.writerow(row[:7] + [action_taken] + row[9:])
    if os.path.exists("output.csv"):
        os.remove("output.csv")




def plot_route(model_episode):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv("log.csv")
    # Group the DataFrame by episode
    grouped = df.groupby('episode')
    print(np.shape(df))
    # Iterate over each episode and plot its x-coordinates and y-coordinates
    for i, (episode, group) in enumerate(grouped):
        if episode in model_episode:
            x = group['xc'].values
            y = group['yc'].values
            plt.scatter(x, y, label=f"Episode {episode}")
    # Add a legend to the plot
    plt.legend()
    # Set the axis labels and title
    plt.xlabel("X-Coordinates")
    plt.ylabel("Y-Coordinates")
    plt.title("X-Y Plot by Episode")
    plt.show()
    # Show the plot

#Todo: TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
#Todo: TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
#Todo: TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO

    #Todo: Add your file path and episodes here

file_path = r"YOUR_PATH_HERE"
episodes =list(range(530,539))

#Todo: TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
#Todo: TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
#Todo: TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO

# Main functionality

clear_log(file_path)
refine_log()
plot_route(episodes)
