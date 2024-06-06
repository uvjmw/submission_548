import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

# Load the lane DataFrame
lane_df = pd.read_csv("C:/Users/ad226/Documents/testfeld_autonomes_fahren_scenarios/scenariodatabase/k733_2020-09-15/local_coordinates_lanes.csv")

# Load the track DataFrame
track_df = pd.read_csv("C:/Users/ad226/Documents/testfeld_autonomes_fahren_scenarios/scenariodatabase/k733_2020-09-15/vehicle_tracks_000.csv")

# Create an empty DataFrame to store the results
result_df = pd.DataFrame(columns=['track_id', 'closest_lane'])