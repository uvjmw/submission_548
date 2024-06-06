
import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv(r'C:\Users\ad226\Documents\testfeld_autonomes_fahren_scenarios\scenariodatabase\k733_2020-09-15\Lanes_localcoordinates.csv')


# Define the point to compare
point_to_compare = (-15, -53)  # Example point to compare (x, y)

# Create an empty dictionary to store the lanes and their respective points
lanes = {}

# Group points by lane
for lane, group in df.groupby('Lane'):
    x_values = group['x'].values
    y_values = group['y'].values
    lanes[lane] = {'x_values': x_values, 'y_values': y_values}

# Interpolate points for each lane
num_points_interpolated = 100  # Adjust as needed
for lane, points in lanes.items():
    x_interpolated = np.linspace(min(points['x_values']), max(points['x_values']), num_points_interpolated)
    y_interpolated = np.interp(x_interpolated, points['x_values'], points['y_values'])
    lanes[lane]['x_interpolated'] = x_interpolated
    lanes[lane]['y_interpolated'] = y_interpolated

# Function to calculate Euclidean distance between two points
def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to find the closest lane to the given point
def find_closest_lane(point, lanes):
    min_distance = float('inf')
    closest_lane = None
    for lane, points in lanes.items():
        for x, y in zip(points['x_interpolated'], points['y_interpolated']):
            distance = euclidean_distance(point, (x, y))
            if distance < min_distance:
                min_distance = distance
                closest_lane = lane
    return closest_lane

# Calculate the closest lane to the given point
closest_lane = find_closest_lane(point_to_compare, lanes)
print(f"The closest lane to the point {point_to_compare} is {closest_lane}")
