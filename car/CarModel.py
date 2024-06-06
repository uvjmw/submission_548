import argparse
import logging
import pathlib
from turtle import st

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go

from rsu.RSUModel import RSUModel
from signaling.SignalModel import SignalModel
from scenariodatabase.DBController import DBController
from scenariodatabase.Entities.Entities import RSUResult


log = logging.getLogger(__name__)
class CarModel:

    def __init__(self, db_file, data_directory: pathlib.Path, data_directory_signal: pathlib.Path, radius: float = 20, routing_id: int=0):
        self.dbc = DBController(db_file)
        if routing_id is not None:
            self.routings = [self.dbc.get_routing_by_id(routing_id=routing_id)]
        else:
            self.routings = self.dbc.get_routings()

        self.dd = data_directory
        self.dds = data_directory_signal
        self.detection_radius=radius



    def simulate_all_scenarios_for_routings(self):
        result_sce_dict = {}

        count = 0
        for routing in self.routings:
            count = count + 1
            scenarios = routing.scenario

            log.info(f'calculating routing {count} / {len(self.routings)} with {len(scenarios)} scenarios')
            signal = self.dbc.get_signal_by_id(routing.rel_signal)

            rsu = RSUModel(signal=signal, data_directory=self.dd, radius=self.detection_radius)
            signaling = SignalModel(data_directory_signal=self.dds)

            sce_count = 0
            for sce in scenarios:
                sce_count = sce_count + 1
                log.info(f'calculating scenario {sce_count} / {len(scenarios)}')
                objects_transmitted, vru_present, vru_located, transmission_successful, ego_pos, vru_present_ground_truth = rsu.request_object_locations(
                    sce)

                signal_state = signaling.request_signal_states(scenario=sce)
                #ego_pos = pd.merge(ego_pos, signal_state)

                unique_states = signal_state['movement_state'].unique()

                if len(unique_states) == 1:
                    rel_state = unique_states[0]
                elif len(unique_states) >= 2:
                    rel_state = f'{unique_states[0]} -> {unique_states[1]}'
                else:
                    rel_state = None

                result = RSUResult(scenario_id=sce.scenario_id,
                                   vru_present_ground_truth=vru_present_ground_truth,
                                   vru_present=vru_present,
                                   vru_located=vru_located,
                                   transmission_successful=transmission_successful,
                                   detection_radius=self.detection_radius,
                                   signal_state=rel_state)
                self.dbc.insert_object(result)
                log.info(f'saving RSU simulation result for {sce.scenario_id}')
                result_sce_dict[sce.scenario_id] = {'objects_transmitted': objects_transmitted,
                                                    'vru_present': vru_present,
                                                    'vru_located': vru_located,
                                                    'transmission_succesful': transmission_successful}
                #self.plot_scenario(sce, ego_pos, objects_transmitted)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Signal parameters parser")
    parser.add_argument("--routing_id", type=int, help="The routing ID (integer)", required=False)
    parser.add_argument("--db-file", type=str, help="The absolute path to the database file")
    parser.add_argument("-dd", type=str, help="The absolute path to the data directory")
    parser.add_argument("-dds", type=str, help="The absolute path to the signaling file")
    parser.add_argument("-r", type=float, help="The radius of the signal (optional)", required=False)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a console handler and set the level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    args = parser.parse_args()
    db_path = pathlib.Path(rf'{args.db_file}')
    data_dir = pathlib.Path(rf'{args.dd}')
    data_dir_signal = pathlib.Path(rf'{args.dds}')
    car_model = CarModel(db_file=db_path, radius=args.r, data_directory=data_dir, data_directory_signal=data_dir_signal, routing_id=args.routing_id)
    car_model.simulate_all_scenarios_for_routings()
