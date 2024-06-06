
import argparse
import pathlib
import os
import plotly.express as px
import pandas as pd




#TODO: auswahl für use-case
#TODO: Abbiegemanöver aussuchen. Alle beteiligten szenarien für fahrzeuge extrahieren
#TODO: Ampel bei szenario fixen
#TODO: rausfinden welche signal group relevant ist

class DataReader:

    def __init__(self, rd):
        self.rd = rd
        self.df_track = None
        self.df_ampel = None

    def main(self):
        self.read_in()
        self.scenariorize()

    def read_in(self):
        files = os.listdir(self.rd)
        files = [file_name for file_name in files if file_name != 'meta_data.csv']

        # test.py
        #files = [files][1:2]

        ampel = True
        if ampel:
            self.df_track = pd.DataFrame(pd.read_csv(self.rd/files[2]))
            self.df_ampel = pd.DataFrame(pd.read_csv(self.rd/files[1]))

        else:
            df = pd.DataFrame()
            for file in files:
                df = pd.concat([df, pd.read_csv(self.rd/file)])

    def scenariorize(self):
        tracks = {id: self.df_track[self.df_track.track_id == id] for id in self.df_track.track_id.unique()}
        for key in tracks.keys():
            ampel_signal = self.df_ampel.loc[tracks[key].timestamp_ms.min() : tracks[key].timestamp_ms.max()]
            ampel_signal = ampel_signal[(ampel_signal['timestamp_ms'] >= tracks[key].timestamp_ms.min()) & (ampel_signal['timestamp_ms'] <= tracks[key].timestamp_ms.max())]
            ampel_signal = ampel_signal[ampel_signal['signal_group_id'] == 1]
            #TODO: Fix indexing
            tracks[key]['ampel_signal'] = ampel_signal['movement_state']

        pass


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-rd', help="Path to the folder that holds the data files.", required=True)

    # read the folder holding the data
    folder = pathlib.Path(argument_parser.parse_args().rd)
    datareader = DataReader(folder).main()



