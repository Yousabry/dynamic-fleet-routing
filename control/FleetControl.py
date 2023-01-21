import random
from typing import List
from control.CrowdControl import CrowdControl
from control.DistanceControl import DistanceControl
from types.Bus import Bus
from types.Request import PassengerRequest
from types.Stop import Stop

random.seed(666)
NUM_SECONDS_IN_DAY = 86400

class FleetControl:
    FLEET_SIZE = 200 # 900
    BATCH_PERIOD_SEC = 30

    def __init__(self, all_stops: List[Stop]) -> None:
        self.request_pool: List[PassengerRequest] = []
        self.busses: List[Bus] = [Bus(i) for i in range(FleetControl.FLEET_SIZE)]

        high_traffic_stops = [s for s in all_stops if s.high_traffic_stop]
        for bus in self.busses:
            bus.current_location = random.choice(high_traffic_stops)

    def begin_simulation(self, crowd_control: CrowdControl, distance_control: DistanceControl):
        for time in range(0, NUM_SECONDS_IN_DAY+1, FleetControl.BATCH_PERIOD_SEC):
            new_requests = crowd_control.pop_new_requests(time)

            # Handle new requests by batch
            self.request_pool += new_requests

            for req in new_requests:
                print(f" time {req.request_time} from {req.start_location.id} to --> {req.destination.id} (takes {distance_control.get_distance(req.start_location,req.destination)} min straight)")
