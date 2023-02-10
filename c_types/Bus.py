from typing import Set
from c_types.Path import Path
from c_types.Request import PassengerRequest
from c_types.Stop import Stop
from geopy import distance as geodistance
from geographiclib.geodesic import Geodesic

from control.config import AVG_AERAL_PACE_KM_SEC, AVG_AERAL_PACE_M_SEC, BATCH_PERIOD_SEC
from util.debug import debug_log
geod = Geodesic.WGS84

class Bus:
    def __init__(self, id: int):
        self.id = id
        self.passenger_requests: Set[PassengerRequest] = set()
        self.path: Path = Path()
        self.current_location: tuple[float, float] = None

    def get_current_passenger_count(self):
        return sum([1 if req.pickup_time else 0 for req in self.passenger_requests])

    def handle_stop_arrival(self, current_time: int):
        if not self.path:
            raise Exception("upcoming stops should not be empty when handle_stop_arrival is called")
        
        current_stop = self.path.pop_front()
        self.current_location = current_stop.coordinates
        debug_log(f"bus {self.id} arrived at stop {current_stop}")

        for req in self.passenger_requests:
            if req.start_location == current_stop and not req.pickup_time:
                req.pickup_time = current_time
                debug_log(f"request {req.id} picked up by bus {self.id}")
            elif req.destination == current_stop and req.pickup_time:
                req.arrival_time = current_time
                debug_log(f"request {req.id} dropped off by bus {self.id}")

        self.passenger_requests = {r for r in self.passenger_requests if not r.arrival_time}

    def on_time_tic(self, current_time: int):
        if not self.path:
            return

        time_to_simulate = BATCH_PERIOD_SEC
        while time_to_simulate > 0:
            if not self.path: break

            start, dest = self.current_location, self.path.peek_front().coordinates
            distance_to_stop = geodistance.distance(start, dest).km
            time_to_stop = distance_to_stop / AVG_AERAL_PACE_KM_SEC

            if time_to_stop <= time_to_simulate:
                self.handle_stop_arrival(current_time)

                time_to_simulate -= time_to_stop
                continue
            
            else:
                # figure out where we are in path to next stop
                #Solve the Inverse problem
                inv = geod.Inverse(start[0],start[1],dest[0],dest[1])
                azi1 = inv['azi1']

                #Solve the Direct problem
                distance_travelled_metres = time_to_simulate * AVG_AERAL_PACE_M_SEC
                dir = geod.Direct(start[0],start[1],azi1, distance_travelled_metres)
                self.current_location = (dir['lat2'],dir['lon2'])

                break

    def add_stop_at_index(self, idx: int, stop: Stop, req: PassengerRequest):
        self.path.add_stop_at_index(idx, stop)
        self.passenger_requests.add(req)

    def append_stop_to_upcoming(self, stop: Stop, req: PassengerRequest):
        self.path.append_stop(stop)
        self.passenger_requests.add(req)

    def append_if_not_already_in_upcoming(self, stop: Stop, req: PassengerRequest):
        self.path.append_stop_if_not_in_path(stop)
        self.passenger_requests.add(req)
    
    # Append stop if it does not already exist after the required predecessor
    def append_after_stop(self, stop: Stop, req: PassengerRequest, needed_pred: Stop):
        self.path.append_stop_after_pred(stop, needed_pred)
        self.passenger_requests.add(req)
