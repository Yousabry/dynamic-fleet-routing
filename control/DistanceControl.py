from typing import List
import os
from c_types.Stop import Stop
from geopy import distance as geodistance
from control.config import KM_TO_MINUTES_MULTIPLE

DATA_PATH = '../data/'
script_dir = os.path.dirname(__file__)

class DistanceControl:
    def __init__(self) -> None:
        self.all_stops: List[Stop] = []
        self.read_stops_from_file()

    def get_travel_distance_km(self, origin: Stop, dest: Stop) -> int:
        return geodistance.distance(origin.coordinates, dest.coordinates).km

    def get_travel_distance_coord(self, origin: tuple[float, float], dest: tuple[float, float]) -> int:
        return geodistance.distance(origin, dest).km

    def get_travel_time_seconds(self, origin: Stop, dest: Stop) -> int:
        return self.get_travel_distance_km(origin, dest) * KM_TO_MINUTES_MULTIPLE * 60
    
    def get_travel_time_seconds_coord(self, origin: tuple[float, float], dest: tuple[float, float]) -> int:
        return self.get_travel_distance_coord(origin, dest) * KM_TO_MINUTES_MULTIPLE * 60

    def read_stops_from_file(self) -> None:
        stops_abs_file_path = os.path.join(script_dir, f"{DATA_PATH}/stops.txt")

        with open(stops_abs_file_path, "r") as stops_file:
            stops_file.readline()

            for stop in stops_file:
                [stop_id,stop_code,stop_name,stop_lat,stop_lon] = stop.strip().split(",")
                self.all_stops.append(Stop(stop_id,stop_code,stop_name,(float(stop_lat),float(stop_lon))))