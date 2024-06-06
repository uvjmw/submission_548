import csv
import pandas as pd

def extract_timestamps():
    track_timestamps = {}

    with open(r'C:\Users\ad226\Documents\testfeld_autonomes_fahren_scenarios\scenariodatabase\k733_2020-09-15\vehicle_tracks_000.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            track_id = int(row[0])
            timestamp_ms = int(row[2])

            if track_id not in track_timestamps:
                track_timestamps[track_id] = {'first_timestamp': timestamp_ms, 'last_timestamp': timestamp_ms}
            else:
                if timestamp_ms < track_timestamps[track_id]['first_timestamp']:
                    track_timestamps[track_id]['first_timestamp'] = timestamp_ms
                if timestamp_ms > track_timestamps[track_id]['last_timestamp']:
                    track_timestamps[track_id]['last_timestamp'] = timestamp_ms

    return track_timestamps

def main():
    track_timestamps = extract_timestamps()
    df = pd.DataFrame(track_timestamps.values(), index=track_timestamps.keys(), columns=['first_timestamp', 'last_timestamp'])
    df.index.name = 'track_id'
    #df.to_csv('output.csv')
    print("DataFrame saved to output.csv:\n", df)
if __name__ == "__main__":
    main()
