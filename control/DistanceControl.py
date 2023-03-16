from typing import List
import os
from c_types.Stop import Stop
from geopy import distance as geodistance
from control.config import AVG_AERAL_PACE_M_SEC, HIGH_TRAFFIC_ZONE_RADIUS_KM, HIGH_TRAFFIC_AREAS, KM_TO_MINUTES_MULTIPLE
from functools import lru_cache
from geographiclib.geodesic import Geodesic

geod = Geodesic.WGS84

DATA_PATH = '../data/'
script_dir = os.path.dirname(__file__)

class DistanceControl:
    def __init__(self) -> None:
        self.all_stops: List[Stop] = []
        self.read_stops_from_file()

    @lru_cache(maxsize=None)
    def get_travel_distance_km(self, origin: Stop, dest: Stop) -> int:
        return geodistance.distance(origin.coordinates, dest.coordinates).km

    @lru_cache(maxsize=None)
    def get_travel_distance_coord(self, origin: tuple[float, float], dest: tuple[float, float]) -> int:
        return geodistance.distance(origin, dest).km

    @lru_cache(maxsize=None)
    def get_travel_time_seconds(self, origin: Stop, dest: Stop) -> int:
        return self.get_travel_distance_km(origin, dest) * KM_TO_MINUTES_MULTIPLE * 60
    
    @lru_cache(maxsize=None)
    def get_travel_time_seconds_coord(self, origin: tuple[float, float], dest: tuple[float, float]) -> int:
        return self.get_travel_distance_coord(origin, dest) * KM_TO_MINUTES_MULTIPLE * 60
    
    # figure out where we are in path to next stop
    def get_new_coord_after_time_travelled(self, start: tuple[float, float], dest: tuple[float, float], time_travelled: int) -> tuple[float, float]:
        # Solve the Inverse problem
        inv = geod.Inverse(start[0],start[1],dest[0],dest[1])
        azi1 = inv['azi1']

        #Solve the Direct problem
        distance_travelled_metres = time_travelled * AVG_AERAL_PACE_M_SEC
        dir = geod.Direct(start[0],start[1], azi1, distance_travelled_metres)
        return (dir['lat2'],dir['lon2'])
    
    def is_high_traffic_stop(self, stop_coord: tuple[float, float]) -> bool:
        for area in HIGH_TRAFFIC_AREAS:
            if self.get_travel_distance_coord(stop_coord, area) <= HIGH_TRAFFIC_ZONE_RADIUS_KM:
                return True
            
        return False

    def read_stops_from_file(self) -> None:
        stops_abs_file_path = os.path.join(script_dir, f"{DATA_PATH}/stops.txt")

        with open(stops_abs_file_path, "r") as stops_file:
            stops_file.readline()

            for stop in stops_file:
                [stop_id,stop_code,stop_name,stop_lat,stop_lon] = stop.strip().split(",")
                stop_coord = (float(stop_lat),float(stop_lon))
                high_traffic_stop = self.is_high_traffic_stop(stop_coord)

                self.all_stops.append(Stop(stop_id,stop_code,stop_name,stop_coord,high_traffic_stop))