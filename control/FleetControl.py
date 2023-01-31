import random
from typing import List
from c_types.Bus import Bus
from c_types.Request import PassengerRequest
from c_types.Stop import Stop
from control.config import FLEET_SIZE


class FleetControl:
    def __init__(self, all_stops: List[Stop]) -> None:
        self.request_pool: List[PassengerRequest] = []
        self.busses: List[Bus] = [Bus(i) for i in range(FLEET_SIZE)]

        high_traffic_stops = [s for s in all_stops if s.high_traffic_stop]
        for bus in self.busses:
            bus.current_location = random.choice(high_traffic_stops).coordinates
