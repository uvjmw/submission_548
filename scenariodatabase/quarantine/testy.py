import csv

import pandas as pd


def extract_timestamps(csv_file):
    track_timestamps = {}

    with open(csv_file, 'r') as file:
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
    csv_file = r'C:\Users\ad226\Documents\testfeld_autonomes_fahren_scenarios\scenariodatabase\k733_2020-09-15\vehicle_tracks_000.csv'
    track_timestamps = extract_timestamps(csv_file)
    df = pd.DataFrame(track_timestamps)

    for track_id, timestamps in track_timestamps.items():
        print(f"Track ID: {track_id}, First Timestamp: {timestamps['first_timestamp']}, Last Timestamp: {timestamps['last_timestamp']}")


if __name__ == "__main__":
    main()
