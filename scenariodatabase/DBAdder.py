import pathlib
import os
import argparse
import logging
import sys
import csv
import pandas as pd
from sqlalchemy import JSON
from scenariodatabase.Entities.Base import Base
from scenariodatabase.Entities.Entities import Scenario, Routing, Lane, Signal
from scenariodatabase.DBController import DBController

# define the logging properties
log = logging.getLogger()
formatter = logging.Formatter('%(asctime)s [%(module)18s][%(levelname)8s] %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)
log.setLevel(logging.INFO)


class ScenarioAdder:
    def __init__(self, db_file):
        self.dbc = DBController(db_file)
        self.dbc.create_session()

    def add_scenarios(self, data_dir):

        csv_files_vehicles = [file for file in os.listdir(data_dir) if file.endswith(".csv") and "vehicle" in file]
        count = 0
        for file in csv_files_vehicles:
            count = count +1
            log.info(f'Adding file {count}/{len(csv_files_vehicles)}')
            df = pd.read_csv(data_dir/file, index_col=False)
            t_min = df['timestamp_ms'].min()
            # Sort DataFrame by 'track_id' and then by 'frame'
            df = df.sort_values(by=['track_id', 'frame_id'])

            # Reset index after sorting
            df.reset_index(drop=True, inplace=True)
            df = df.iloc[:, 1:]

            for track_id in df['track_id'].unique():
                track = df[df['track_id'] == track_id]

                scenario = Scenario(
                    track_id=int(track_id),
                    start_time=(track['timestamp_ms'].min() - t_min) / 1000,
                    end_time=(track['timestamp_ms'].max() - t_min) / 1000,
                    file=file,
                    signal_file='signal' + file[7:],
                    type=track['agent_type'][track.index[0]]

                )
                self.dbc.insert_object(scenario)
                #self.dbc.session.commit()

    def add_lanes(self):

        #https://odrviewer.io/
        lanes_x_min = [26.5, 23.1, 7.5, 7.5, 7.5, 7.5, 23, 26.5, 30, 33.5, 42, 42, 42, 42, 30, 33.6]
        lanes_x_max = [29.7, 26.2, 17.7, 17.7, 17.7, 17.7, 26.2, 29.6, 33.2, 36.7, 52, 52, 52, 52, 33.1, 36.8]
        lanes_y_min = [-112, -112, -96.7, -93.2, -89.6, -86.1, -76, -76, -76, -76, -86.6, -90, -93.6, -97, -112, -112]
        lanes_y_max = [-102, -102, -93.5, -90.1, -86.4, -83.1, -66, -66, -66, -66, -83.6, -86.9, -90.4, -93.9, -102, -102]


        for i in range(len(lanes_y_max)):
            lane = Lane(lane_id=i+1,
                        x_min=lanes_x_min[i],
                        x_max=lanes_x_max[i],
                        y_min=lanes_y_min[i],
                        y_max=lanes_y_max[i]
                        )

            self.dbc.insert_object(lane)


    def add_routings(self):
        lane_start = [3, 3, 3, 4, 4, 4, 7, 7, 7, 8, 8, 8, 11, 11, 11, 12, 12, 12, 15, 15, 15, 16, 16, 16]
        lane_end = [14, 2, 10, 13, 1, 9, 2, 6, 14, 1, 5, 13, 6, 10, 2, 5, 9, 1, 10,  14, 6, 9, 13, 5]
        rel_signal = [1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2]

        #TODO relevant signal definition

        for i in range(len(lane_end)):
            routing = Routing(
                start_lane=lane_start[i],
                end_lane=lane_end[i],
                rel_signal=rel_signal[i]
            )

            self.dbc.insert_object(routing)

    def add_signals(self, data_dir):
        signal_ids = [1, 2, 3, 4]
        x_pos = [-7.993302822113037, -6.946513652801514, -7.2239, -7.219]
        y_pos = [29.35050773620605, 29.900436401367188, 30.4, 30.55]

        for i in range(len(signal_ids)):
            signal = Signal(
                signal_id=signal_ids[i],
                signal_position_x=x_pos[i],
                signal_position_y=y_pos[i]
            )
            self.dbc.insert_object(signal)

        """
        csv_files_signals = [file for file in os.listdir(data_dir) if file.endswith(".csv") and "signal" in file]

        ids = []
        for file in csv_files_signals:
            df = pd.read_csv(data_dir/file)
            for uni in df['signal_group_id'].unique().tolist():
                if uni not in ids:
                    ids.append(uni)
                    signal = Signal(
                        signal_id=uni,
                        signal_position_x=df[df['signal_group_id'] == uni].pos_x.min(),
                        signal_position_y=df[df['signal_group_id'] == uni].pos_y.min()
                    )
                    self.dbc.insert_object(signal)
            pass
        """



if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        description="Adds Scenario to the Database")
    argument_parser.add_argument('--db-file', help="path to db-file", required=True)
    argument_parser.add_argument('--data-dir', help="path to data", required=True)

    # directory where dataset is found, data set name will be appended
    db_file = pathlib.Path(argument_parser.parse_args().db_file)
    data_dir = pathlib.Path(argument_parser.parse_args().data_dir)

    log.info(f'Using Database {db_file.stem}')
    adder = ScenarioAdder(db_file)
    adder.add_scenarios(data_dir)
    adder.add_lanes()
    adder.add_routings()
    adder.add_signals(data_dir)