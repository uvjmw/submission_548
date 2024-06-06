import csv
import pandas as pd
import pathlib
import os
import argparse
import logging
import sys

from sqlalchemy import JSON

from scenariodatabase.Entities.Base import Base
from scenariodatabase.Entities.Entities import Scenario, Routing, Lane, Signal
from scenariodatabase.DBController import DBController

log = logging.getLogger()
formatter = logging.Formatter('%(asctime)s [%(module)18s][%(levelname)8s] %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)
log.setLevel(logging.INFO)


class DataReader:

    def __init__(self, db_file):
        self.dbc = DBController(db_file)
        self.dbc.create_session()

    def signal_reader(self):
        file_path = 'C:/Users/ad226\Documents/testfeld_autonomes_fahren_scenarios/scenariodatabase/k733_2020-09-15/signal_phases_000.csv'
        df = pd.read_csv(file_path)
        signals = df['signal_group_id'].unique()
        return signals

    def add_signals(self, signal_id: int):
        signal = Signal(
            signal_id=signal_id
        )
        self.dbc.insert_signal(signal)

    def commit_new_signal(self):
        self.dbc.session.commit()

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        description="Adds Signals to the Database from file")
    argument_parser.add_argument('--db-file', help="data directory, where original dataset is placed.", required=True)

    # directory where dataset is found, data set name will be appended
    db_file = pathlib.Path(argument_parser.parse_args().db_file)
    log.info(f'Using Database {db_file.stem}')
    adder = DataReader(db_file)
    signals = adder.signal_reader()
    my_array_as_integers = [int(item) for item in signals]
    for item in my_array_as_integers:
        adder.add_signals(item)
        adder.commit_new_signal()
