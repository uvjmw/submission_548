import argparse
import logging
import pathlib


from scenariodatabase.DBController import DBController
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots



class VisualizeAggregatedResults:

    def __init__(self, db_file):
        self.dbc = DBController(db_file)
        pass

    def aggregate_by_routing_id(self, routing_id):
        scenarios = self.dbc.get_scenarios_by_routing_id(routing_id)
        routing = self.dbc.get_routing_by_id(routing_id)
        scenarios = routing.scenario

        rsuresults = []
        for sce in scenarios:
            rsuresults.append(self.dbc.get_rsuresult_by_scenario_id(sce.scenario_id))

        return rsuresults

    def driving_mode_histogramm(self, routing_id:int):
        rsuresults = self.aggregate_by_routing_id(routing_id)

        driving_mode_dict = {}
        driving_mode_dict['profile 1'] = []
        driving_mode_dict['profile 2'] = []
        driving_mode_dict['profile 3'] = []


        for result in rsuresults:
            if not result[0].transmission_successful:
                driving_mode_dict['profile 1'].append(result)
            else:
                if not result[0].vru_present:
                    driving_mode_dict['profile 2'].append(result)
                else:
                    if not result[0].vru_located:
                        driving_mode_dict['profile 1'].append(result)
                    else:
                        driving_mode_dict['profile 3'].append(result)

        # Get the count of entries in each list
        count_data = {mode: len(results) for mode, results in driving_mode_dict.items()}

        # Create a DataFrame from the count data
        df_count = pd.DataFrame(list(count_data.items()), columns=['Driving Mode', 'Count'])

        # Sort DataFrame by count in descending order
        df_count = df_count.sort_values(by='Count', ascending=False)

        # Calculate the percentage for each step
        total_scenarios = sum(df_count['Count'])
        df_count['Percentage'] = (df_count['Count'] / total_scenarios) * 100
        df_count['Cumulative Percentage'] = df_count['Percentage'].cumsum()

        # Create figure with secondary y-axis
        fig = go.Figure()

        # Plot Number of Entries
        fig.add_trace(go.Bar(x=df_count['Driving Mode'], y=df_count['Count'],
                             marker_color='blue', name='Number of Entries', yaxis='y'))

        # Plot Cumulative Percentage
        fig.add_trace(go.Scatter(x=df_count['Driving Mode'], y=df_count['Cumulative Percentage'],
                                 mode='lines+markers', marker=dict(color='red'), name='Cumulative Percentage',
                                 yaxis='y2'))

        # Update layout
        fig.update_layout(title_text=f'Number of Entries and Cumulative Saturation Curve of Driving Modes for routing {routing_id}',
                          xaxis_title_text='Driving Modes',
                          yaxis_title_text='Number of Entries',
                          yaxis2=dict(title='Cumulative Percentage', overlaying='y', side='right', range=[0, 105]),
                          showlegend=True)

        # Show the plot
        fig.show()
        pass

    def coverage_analysis(self):
        results = self.dbc.get_rsuresults()
        signal_states = ['Red', 'Green', 'Yellow', 'Red -> Green', 'Green -> Red', 'Green -> Yellow', 'Yellow -> Red', 'None']
        vru_present = [False, True]
        vru_located = [False, True]
        transmission_successful = [False, True]
        combinations = {}

        for i in range(0,8):
            for j in range(0,2):
                for k in range(0,2):
                    for l in range(0,2):
                        key = f'{i}-{j}-{k}-{l}'
                        combinations[key] = []


        for res in results:
            state = signal_states.index(f'{res.signal_state}')
            key = f'{state}-{vru_present.index(res.vru_present)}-{vru_located.index(res.vru_located)}-{transmission_successful.index(res.transmission_successful)}'
            combinations[key].append(res)


        # Extract the lengths of the lists and the keys
        keys = list(combinations.keys())
        lengths = []
        for val in combinations.values():
            lengths.append(len(val))

        # Define color mapping based on the first digit of the key
        color_mapping = {
            '0': 'red',
            '1': 'green',
            '2': 'yellow',
            '3': 'red',
            '4': 'green',
            '5': 'yellow',
            '6': 'orange',
            '7': 'gray'
        }

        # Create a figure to hold the bars
        fig = go.Figure()

        # Add bars with labels and colors, grouping them in the legend by the first digit
        for key, length in zip(keys, lengths):
            first_digit = key[0]
            color = color_mapping.get(first_digit, 'black')  # Get color based on the first digit
            if not any(trace.name.startswith(first_digit) for trace in fig.data):
                fig.add_trace(
                    go.Bar(name=f'Group {first_digit}', showlegend=True))  # Add group to legend if not already present
            fig.add_trace(go.Bar(x=[key], y=[length], name=f'{key}: {length}', marker=dict(color=color)))

        # Update layout
        fig.update_layout(
            title='Number of scenarios for each combination of subsystem states',
            yaxis=dict(title='Number of scenarios'),
            xaxis=dict(title='Combination of states')
        )

        # Show plot
        fig.show()



        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Signal parameters parser")
    parser.add_argument("--routing_id", type=int, help="The routing ID (integer)")
    parser.add_argument("--db-file", type=str, help="The absolute path to the database file")

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
    db_file = pathlib.Path(rf'{args.db_file}')

    visualizer = VisualizeAggregatedResults(db_file=db_file)
    visualizer.coverage_analysis()

    #for i in range(1, 24):
    #    visualizer.driving_mode_histogramm(i)#(args.routing_id)
