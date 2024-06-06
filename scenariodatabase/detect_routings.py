import pathlib
import os
import argparse
import logging
import sys
import numpy as np
import csv
import pandas as pd
from scenariodatabase.DBController import DBController
from scenariodatabase.ScenarioGetter import ScenarioGetter
import plotly.express as px

# define the logging properties
log = logging.getLogger()
formatter = logging.Formatter('%(asctime)s [%(module)18s][%(levelname)8s] %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)
log.setLevel(logging.INFO)


class RoutingCalculator:
    def __init__(self, db_file, dd):
        self.dbc = DBController(db_file)
        self.dbc.create_session()
        self.dd = dd
        self.lane_list = self.dbc.get_lanes()

    def main(self):
        scenarios = self.dbc.get_scenarios_by_type('car')
        scenarios.extend(self.dbc.get_scenarios_by_type('van'))
        scenarios.extend(self.dbc.get_scenarios_by_type('truck'))

        count = 0
        for sce in scenarios:
            with ScenarioGetter(sce, self.dd) as getter:
                ego_pos = getter.get_ego_position()

                lanes = []
                for lane in self.lane_list:

                    filtered_indices = ego_pos[
                        (ego_pos['x'] >= lane.x_min) & (ego_pos['x'] <= lane.x_max) &
                        (ego_pos['y'] >= lane.y_min) & (ego_pos['y'] <= lane.y_max)
                        ]
                    if not filtered_indices.empty:
                        lanes.append(lane.lane_id)

                if len(lanes) == 2:
                    try:
                        if lanes[0] not in [3,4,7,8,11,12,15,16]:
                            routing = self.dbc.get_routing_by_lanes(lanes[1], lanes[0])
                        else:
                            routing = self.dbc.get_routing_by_lanes(lanes[0], lanes[1])
                        if routing is not None:
                            count = count +1
                            sce.ego_routing = routing.routing_id
                            self.dbc.insert_object(sce)
                    except UnboundLocalError:
                        log.info(f'no routing for sce {sce.scenario_id}')
        log.info(f' found {count} routings for {len(scenarios)} scenarios')


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        description="Adds Scenario to the Database")
    argument_parser.add_argument('--db-file', help="path to db-file", required=True)
    argument_parser.add_argument('--data-dir', help="path to data", required=True)

    # directory where dataset is found, data set name will be appended
    db_file = pathlib.Path(argument_parser.parse_args().db_file)
    data_dir = pathlib.Path(argument_parser.parse_args().data_dir)

    log.info(f'Using Database {db_file.stem}')
    routing_calculator = RoutingCalculator(db_file, data_dir).main()
