from typing import List, Set
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
        self.upcoming_stops: List[Stop] = []
        self.current_location: tuple[float, float] = None

    def get_current_passenger_count(self):
        return sum([1 if req.pickup_time else 0 for req in self.passenger_requests])

    def update_current_position(self, current_time: int):
        if not self.upcoming_stops:
            return

        time_to_simulate = BATCH_PERIOD_SEC
        while time_to_simulate > 0:
            if not self.upcoming_stops: break

            start, dest = self.current_location, self.upcoming_stops[0].coordinates
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

    def handle_stop_arrival(self, current_time: int):
        if len(self.upcoming_stops) == 0:
            raise Exception("upcoming stops should not be empty when handle_stop_arrival is called")
        current_stop = self.upcoming_stops[0]
        debug_log(f"bus {self.id} arrived at stop {current_stop}")

        for req in self.passenger_requests:
            if req.start_location == current_stop and not req.pickup_time:
                req.pickup_time = current_time
                debug_log(f"request {req.id} picked up by bus {self.id}")
            elif req.destination == current_stop and req.pickup_time:
                req.arrival_time = current_time
                debug_log(f"request {req.id} dropped off by bus {self.id}")

        self.passenger_requests = {r for r in self.passenger_requests if not r.arrival_time}
        self.current_location = current_stop.coordinates
        self.upcoming_stops.pop(0)

    def on_time_tic(self, current_time: int):
        if not self.upcoming_stops:
            return

        self.update_current_position(current_time)

    def add_stop_at_index(self, idx: int, stop: Stop, req: PassengerRequest):
        if idx >= len(self.upcoming_stops):
            self.append_stop_to_upcoming(stop, req)
            return
        
        predecessor_idx, successor_idx = idx - 1, idx
        
        # we never want the same stop listed twice consecutively
        if predecessor_idx >= 0 and self.upcoming_stops[predecessor_idx] == stop:
            return
        
        if successor_idx < len(self.upcoming_stops) and self.upcoming_stops[successor_idx] == stop:
            return

        self.upcoming_stops.insert(idx, stop)
        self.passenger_requests.add(req)

    def append_stop_to_upcoming(self, stop: Stop, req: PassengerRequest):
        predecessor_idx = len(self.upcoming_stops) - 1

        if predecessor_idx >= 0 and self.upcoming_stops[predecessor_idx] == stop:
            return
        
        self.upcoming_stops.append(stop)
        self.passenger_requests.add(req)

    def append_if_not_already_in_upcoming(self, stop: Stop, req: PassengerRequest):
        if stop in self.upcoming_stops:
            return
        
        self.append_stop_to_upcoming(stop, req)
    
    # Append stop if it does not already exist after the required predecessor
    def append_after_stop(self, stop: Stop, req: PassengerRequest, needed_pred: Stop):
        pred_idx = self.upcoming_stops.index(needed_pred)

        if stop in self.upcoming_stops[pred_idx:]:
            return
        
        self.append_stop_to_upcoming(stop, req)

    # def do_stops_satisfy_requests(stops_planned: List[Stop]) -> bool:
    # for each req make sure first instance of start_location appears before last instance of destination
    #     return False

    # # TODO: careful, this includes destination stops for reqs that might not have been picked up yet...
    # def get_requests_that_need_stop(self, stop: Stop) -> List[PassengerRequest]:
    #     return [req for req in self.passenger_requests if stop in [req.start_location, req.destination]]

    # def get_passenger_count_change_at_stop(self, stop: Stop) -> int:
    #     reqs = self.get_requests_that_need_stop(stop)
    #     return sum([1 if req.start_location == stop else -1 for req in reqs])
