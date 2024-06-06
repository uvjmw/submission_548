import logging
import pathlib
import sys

import pandas as pd

log = logging.getLogger(__name__)
class ScenarioGetter:

    def __init__(self, scenario, dd):
        self.sce = scenario

        try:
            self.data_df = pd.read_csv(pathlib.Path(dd, self.sce.file))
            self.data_df['timestamp_ms'] = (self.data_df['timestamp_ms'] - self.data_df['timestamp_ms'].min()) / 1000
        except OSError as e:
            log.critical("Could not open file %s . Exiting.", str(self.sce.file))
            log.exception(e)
            sys.exit(1)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        log.debug("Exit called. File will be closed.")

    def get_ego_position(self):
        ego_pos = self.data_df[self.data_df['track_id'] == self.sce.track_id]
        return ego_pos

    def get_objects_in_scenario(self):
        mask = (self.data_df['timestamp_ms'] >= self.sce.start_time) & (self.data_df['timestamp_ms'] <= self.sce.end_time) & (
                    self.data_df['track_id'] != self.sce.track_id)
        objects = self.data_df[mask]
        return objects
