from typing import Set
from c_types.Path import Path
from c_types.Request import PassengerRequest
from c_types.Stop import Stop
from control.DistanceControl import DistanceControl

from control.config import BATCH_PERIOD_SEC
from util.debug import debug_log

class Bus:
    def __init__(self, id: int):
        self.id = id
        self.passenger_requests: Set[PassengerRequest] = set()
        self.path: Path = Path()
        self.current_location: tuple[float, float] = None
        self.current_passenger_count: int = 0
        self.stops_visited: list[Stop] = []

    def handle_stop_arrival(self, current_time: int):        
        current_stop = self.path.pop_front()
        self.current_location = current_stop.coordinates
        self.stops_visited.append(current_stop)
        debug_log(f"bus {self.id} arrived at stop {current_stop}")

        for req in self.passenger_requests:
            if req.start_location == current_stop and not req.pickup_time:
                req.pickup_time = current_time
                self.current_passenger_count += 1
                debug_log(f"request {req.id} picked up by bus {self.id}")
            elif req.destination == current_stop and req.pickup_time:
                req.arrival_time = current_time
                self.current_passenger_count -= 1
                req.serving_bus_id = self.id
                debug_log(f"request {req.id} dropped off by bus {self.id}")

        self.passenger_requests = {r for r in self.passenger_requests if not r.arrival_time}

    def on_time_tic(self, current_time: int, dc: DistanceControl):
        if not self.path: return

        time_to_simulate = BATCH_PERIOD_SEC
        while time_to_simulate > 0:
            if not self.path: break

            start, dest = self.current_location, self.path.peek_front().coordinates
            time_to_stop = dc.get_travel_time_seconds_coord(start, dest)

            if time_to_stop <= time_to_simulate:
                self.handle_stop_arrival(current_time)

                time_to_simulate -= time_to_stop
                continue
            
            else:
                self.current_location = dc.get_new_coord_after_time_travelled(start, dest, time_to_simulate)
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
