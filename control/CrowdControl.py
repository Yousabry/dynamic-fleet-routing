import random
from typing import List
from c_types.Request import PassengerRequest

from c_types.Stop import Stop

random.seed(666)
NUM_SECONDS_IN_DAY = 86400

class CrowdControl:
    NUM_REQUESTS = 100 # 300_000

    def __init__(self, all_stops: List[Stop]) -> None:
        self.passenger_requests: List[PassengerRequest] = []
        self.prev_batch_end_index: int = -1
        self.prepare_requests(all_stops)

    def prepare_requests(self, all_stops: List[Stop]) -> None:
        for i in range(CrowdControl.NUM_REQUESTS):
            # TODO: add weight for high volume stops and high volume times
            [start_location, destination] = random.sample(all_stops, 2)
            request_time = random.randint(0, NUM_SECONDS_IN_DAY)

            self.passenger_requests.append(PassengerRequest(i, start_location, destination, request_time))
        
        self.passenger_requests = sorted(self.passenger_requests, key=lambda req: req.request_time)

    def pop_new_requests(self, time: int) -> List[PassengerRequest]:
        new_requests = []

        for i in range(self.prev_batch_end_index + 1, len(self.passenger_requests)):
            if self.passenger_requests[i].request_time <= time:
                new_requests.append(self.passenger_requests[i])
            else:
                self.prev_batch_end_index = i - 1
                break
        
        return new_requests