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

    def plot_scenario(self, scenario, ego_pos, objects_transmitted):

        df = objects_transmitted
        # Create a figure
        fig = go.Figure()

        #---------------------------------- RSU Plot---------------------------------------
        rsu_x = -20
        rsu_y = -20
        # Plot the RSU location
        fig.add_trace(go.Scatter(x=[rsu_x], y=[rsu_y], mode='markers', marker=dict(color='red'), name='RSU Location'))

        # Plot the detection radius as a dashed circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x_circle = rsu_x + self.detection_radius * np.cos(theta)
        y_circle = rsu_y + self.detection_radius * np.sin(theta)

        fig.add_trace(go.Scatter(x=x_circle, y=y_circle, mode='lines', line=dict(dash='dash'), name='Detection Radius'))

        # ---------------------------------- Ego Plot---------------------------------------

        fig.add_trace(go.Scatter(x=ego_pos['x'], y=ego_pos['y'],
                                 mode='lines', line=dict(color='red', width=3), name='Ego Position'))


        # ---------------------------------- Object Plot---------------------------------------

        # Loop through unique track_ids and add a trace for each track
        for track_id in df['track_id'].unique():
            track_data = df[df['track_id'] == track_id]

            # Separate data based on 'within_rsu_radius'
            within_radius = track_data[track_data['within_rsu_radius']]
            outside_radius = track_data[~track_data['within_rsu_radius']]

            # Plot lines within the radius in color
            fig.add_trace(go.Scatter(x=within_radius['x'], y=within_radius['y'],
                                     mode='lines', line=dict(color='blue'), name=f'Track {track_id} within RSU Radius'))

            # Plot lines outside the radius in grey
            if not outside_radius.empty:
                fig.add_trace(go.Scatter(x=outside_radius['x'], y=outside_radius['y'],
                                         mode='lines', line=dict(color='grey', dash='dash'),
                                         name=f'Track {track_id} outside RSU Radius'))

        # ---------------------------------- Map Plot---------------------------------------
        self.visualize_on_map(objects_transmitted)



        # ---------------------------------- Layout---------------------------------------
        # Set layout
        fig.update_layout(title=f'Individual Tracks for Scenario {scenario.scenario_id}',
                          xaxis=dict(title='X-position', scaleanchor='y', scaleratio=1, range=[-100, 50]),
                          yaxis=dict(title='Y-position', scaleanchor='x', scaleratio=1, range=[-100, 50]))

        # Show the figure
        fig.show()
        pass

    # Code von Joshua
    # https://plotly.com/python/scattermapbox/

    def visualize_on_map(self, objects):


        # Sample data for two trajectories with timestamps and track_id
        trajectory_1 = {
            'lat': [49.005617, 49.005496, 49.005326, 49.005150],
            'long': [8.438189, 8.437950, 8.437637, 8.437243],
            'track_id': [1, 1, 1, 1]}

        trajectory_2 = {
            'lat': [49.005083, 49.005173, 49.005280, 49.005397],
            'long': [8.438330, 8.437749, 8.437190, 8.436607],
            'track_id': [2, 2, 2, 2]}

        # Creating DataFrames for each trajectory
        df_trajectory_1 = pd.DataFrame(trajectory_1)
        df_trajectory_2 = pd.DataFrame(trajectory_2)

        # Combine the trajectories into a single DataFrame called 'objects'
        objects = pd.concat([df_trajectory_1, df_trajectory_2])

        # Resetting index for a cleaner DataFrame
        objects.reset_index(level=0, inplace=True)
        objects.rename(columns={'level_0': 'trajectory'}, inplace=True)
        pass


        # Calculate the bounding box
        lon_min = objects["long"].min()
        lon_max = objects["long"].max()
        lat_min = objects["lat"].min()
        lat_max = objects["lat"].max()

        # Calculate the center coordinates
        center_lon = (lon_min + lon_max) / 2
        center_lat = (lat_min + lat_max) / 2

        # Calculate the zoom level
        lon_range = lon_max - lon_min
        lat_range = lat_max - lat_min
        padding = 0.1  # Add some padding to the zoom level
        zoom = 22 - max(lon_range, lat_range) / padding

        color_list = plotly.colors.qualitative.Dark24 + plotly.colors.qualitative.Dark24_r + plotly.colors.qualitative.Plotly
        fig = go.Figure()

        for track in objects['track_id'].unique():
            df_id = objects[objects["track_id"] == track]
            fig.add_trace(
                go.Scattermapbox(
                    name=f"Track: {int(track)}",
                    mode="lines",
                    lon=df_id["long"],
                    lat=df_id["lat"],
                    line=go.scattermapbox.Line(color=color_list[int(track)], width=3),
                    hovertemplate=f"Track: {int(track)}"

                )
            )

        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_center_lon=center_lon,
            mapbox_center_lat=center_lat,
            mapbox_zoom=zoom,
            margin=dict(l=20, r=20, t=20, b=20),
        )
        return fig


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
