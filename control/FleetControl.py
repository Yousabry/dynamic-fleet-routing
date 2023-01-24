import random
from typing import List
from c_types.Bus import Bus
from c_types.Request import PassengerRequest
from c_types.Stop import Stop

random.seed(666)
NUM_SECONDS_IN_DAY = 86400

class FleetControl:
    FLEET_SIZE = 20 # 900
    BATCH_PERIOD_SEC = 30

    def __init__(self, all_stops: List[Stop]) -> None:
        self.request_pool: List[PassengerRequest] = []
        self.busses: List[Bus] = [Bus(i) for i in range(FleetControl.FLEET_SIZE)]

        high_traffic_stops = [s for s in all_stops if s.high_traffic_stop]
        for bus in self.busses:
            bus.current_location = random.choice(high_traffic_stops)
