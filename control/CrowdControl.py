from random import sample, randint
from typing import List
from c_types.Request import PassengerRequest

from c_types.Stop import Stop
from control.DistanceControl import DistanceControl
from control.config import HIGH_TRAFFIC_STOPS_WEIGHT, MIN_REQUEST_DISTANCE_KM, NUM_REQUESTS, NUM_SECONDS_IN_DAY

class CrowdControl:
    def __init__(self, dc: DistanceControl) -> None:
        self.passenger_requests: List[PassengerRequest] = []
        self.prev_batch_end_index: int = -1
        self.prepare_requests(dc)

    def prepare_requests(self, dc: DistanceControl) -> None:
        all_stops: List[Stop] = dc.all_stops
        stop_weights = [HIGH_TRAFFIC_STOPS_WEIGHT if s.high_traffic_stop else 1 for s in all_stops]

        for i in range(NUM_REQUESTS):
            [start, dest] = self.create_random_request_path(dc, stop_weights)
            request_time = randint(0, NUM_SECONDS_IN_DAY)

            self.passenger_requests.append(PassengerRequest(i, start, dest, request_time, dc))
        
        self.passenger_requests = sorted(self.passenger_requests, key=lambda req: req.request_time)

    def pop_new_requests(self, time: int) -> List[PassengerRequest]:
        new_requests = []

        for i in range(self.prev_batch_end_index + 1, len(self.passenger_requests)):
            if self.passenger_requests[i].request_time <= time:
                new_requests.append(self.passenger_requests[i])
                self.prev_batch_end_index = i
            else:
                break
        
        return new_requests
    
    def create_random_request_path(self, dc: DistanceControl, stop_weights: List[int]) -> List[Stop]:
        [start, dest] = sample(dc.all_stops, 2, counts=stop_weights)

        if start.stop_id == dest.stop_id:
            return self.create_random_request_path(dc, stop_weights)
        
        if dc.get_travel_distance_km(start, dest) < MIN_REQUEST_DISTANCE_KM:
            return self.create_random_request_path(dc, stop_weights)
        
        return [start, dest]