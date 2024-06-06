import argparse
import pandas as pd

from rsu.RSULocalisation import RSULocalisation
from rsu.RSUTransmission import RSUTransmission
from scenariodatabase.Entities.Entities import Scenario
from scenariodatabase.ScenarioGetter import ScenarioGetter



class RSUModel:

    def __init__(self, signal, data_directory, radius: float = 20):
        self.localisation = RSULocalisation(signal=signal, radius=radius)
        self.transmission = RSUTransmission()
        self.dd = data_directory
        pass

    def request_object_locations(self, scenario:Scenario):
        with ScenarioGetter(scenario, self.dd) as getter:
            ego_pos = getter.get_ego_position()
            objects = getter.get_objects_in_scenario()

        #Objects sanity check -  mindestlänge, mindestdauer
        # Group by track_id and apply the function to calculate properties
        if not objects.empty:
            track_properties = objects.groupby('track_id').apply(lambda group: pd.Series({
                'duration': group['timestamp_ms'].max() - group['timestamp_ms'].min(),
                'distance': ((group['x'].diff() ** 2 + group['y'].diff() ** 2) ** 0.5).sum()
            }))

            # Set thresholds for duration and distance
            duration_threshold = 1  # in seconds
            distance_threshold = 2  # adjust based on your requirements

            # Filter track_ids based on the thresholds
            valid_tracks = track_properties[(track_properties['duration'] >= duration_threshold) & (
                        track_properties['distance'] >= distance_threshold)].index

            # Filter the original DataFrame based on valid track_ids
            objects = objects[objects['track_id'].isin(valid_tracks)]

        #Ground truth if objects are there
        if objects.empty:
            vru_present_ground_truth = False
        else:
            vru_present_ground_truth = True

        objects_in_scenario = self.localisation.locate_objects(scenario, objects)
        objects_transmitted, vru_present, vru_located, transmission_successful = self.transmission.transmit_object_list(
            objects_in_scenario)
        return objects_transmitted, vru_present, vru_located, transmission_successful, ego_pos, vru_present_ground_truth


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Signal parameters parser")
    parser.add_argument("--signal_group", type=int, help="The signal group ID (integer)")
    parser.add_argument("-r", type=float, help="The radius of the signal (optional)", required=False)

    args = parser.parse_args()
    rsu = RSUModel(signal_group=args.signal_group, radius=args.r)
    rsu.request_object_locations()
