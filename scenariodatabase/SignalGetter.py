import logging
import pathlib
import sys

import pandas as pd

log = logging.getLogger(__name__)


class SignalGetter:

    def __init__(self, dds):
        self.dds = dds

    def __enter__(self):
        return self

    def __exit__(self, *_):
        log.debug("Exit called. File will be closed.")

    def get_signals_in_scenario(self, scenario):
        try:
            signals = pd.read_csv(pathlib.Path(self.dds/scenario.signal_file))
        except OSError as e:
            log.critical("Could not open file %s . Exiting.")
            log.exception(e)
            sys.exit(1)

        # Filter based on time range and scenario.routing.rel_signal
        signals['timestamp_ms'] = (signals['timestamp_ms'] - signals['timestamp_ms'].min()) / 1000

        x_pos = scenario.routing.signal.signal_position_x
        y_pos = scenario.routing.signal.signal_position_y
        threshold = 0.01

        routing_filtered = signals[(abs(signals['pos_x'] - x_pos) <= threshold) & (abs(signals['pos_y'] - y_pos) <= threshold)]

        time_filtered = routing_filtered.loc[
            (routing_filtered['timestamp_ms'] >= scenario.start_time) & (routing_filtered['timestamp_ms'] <= scenario.end_time)]
        signal_state = time_filtered[['timestamp_ms', 'movement_state']].reset_index(drop=True)

        return signal_state
