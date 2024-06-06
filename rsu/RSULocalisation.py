import numpy as np
from scenariodatabase.Entities.Entities import Signal
import plotly.graph_objects as go

class RSULocalisation:
    def __init__(self, signal:Signal, radius:float=20):
        self.signal = signal
        self.detection_radius = radius

    def locate_objects(self, scenario, objects):
        objects = objects
        #TODO Position aus signal
        rsu_x = -20
        rsu_y = -20

        # Use a lambda function to check if each point is within the detection radius
        objects['within_rsu_radius'] = objects.apply(
            lambda row: ((row['x'] - rsu_x) ** 2 + (row['y'] - rsu_y) ** 2) ** 0.5 <= self.detection_radius, axis=1)

        return objects
