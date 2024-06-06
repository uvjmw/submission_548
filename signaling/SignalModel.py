import pandas as pd

from scenariodatabase.Entities.Entities import Scenario
from scenariodatabase.SignalGetter import SignalGetter

class SignalModel:

    def __init__(self, data_directory_signal):
        self.dds = data_directory_signal
        pass

    def request_signal_states(self, scenario:Scenario):
        with SignalGetter(self.dds) as getter:
            signals = getter.get_signals_in_scenario(scenario)
        return signals

