from typing import List
from control.DistanceControl import DistanceControl
from c_types.Request import PassengerRequest
from c_types.Stop import Stop

class Bus:
    # TODO: implement capacity limit
    BUS_CAPACITY = 25

    def __init__(self, id: int):
        self.id = id
        self.passenger_requests: List[PassengerRequest] = []
        self.upcoming_stops: List[Stop] = []
        self.time_to_next_stop: int = 0
        self.current_location: Stop = None

    def get_current_passenger_count(self):
        return sum([1 if req.pickup_time else 0 for req in self.passenger_requests])

    def on_time_tic(self, current_time: int, distance_control: DistanceControl):
        if self.time_to_next_stop == 0:
            return

        self.time_to_next_stop -= 1

        if self.time_to_next_stop == 0:
            if len(self.upcoming_stops) == 0:
                raise Exception("upcoming stops should not be empty if time to next stop is non-zero.")

            self.current_location = self.upcoming_stops.pop(0)
            print(f"bus {self.id} arrived at stop {self.current_location}")

            for req in self.passenger_requests:
                if req.start_location == self.current_location and not req.pickup_time:
                    req.pickup_time = current_time
                    print(f"request {req.id} picked up by bus {self.id}")
                elif req.destination == self.current_location and req.pickup_time:
                    req.arrival_time = current_time
                    print(f"request {req.id} dropped off by bus {self.id}")

            self.passenger_requests = [r for r in self.passenger_requests if r.arrival_time and r.arrival_time < current_time]

            # what to do after
            if self.upcoming_stops:
                self.time_to_next_stop = distance_control.get_distance(self.current_location, self.upcoming_stops[0])

    # def do_stops_satisfy_requests(stops_planned: List[Stop]) -> bool:
    # for each req make sure first instance of start_location appears before last instance of destination
    #     return False

    # # TODO: careful, this includes destination stops for reqs that might not have been picked up yet...
    # def get_requests_that_need_stop(self, stop: Stop) -> List[PassengerRequest]:
    #     return [req for req in self.passenger_requests if stop in [req.start_location, req.destination]]

    # def get_passenger_count_change_at_stop(self, stop: Stop) -> int:
    #     reqs = self.get_requests_that_need_stop(stop)
    #     return sum([1 if req.start_location == stop else -1 for req in reqs])
