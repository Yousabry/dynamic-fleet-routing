from typing import List
from types.Request import PassengerRequest
from types.Stop import Stop

class Bus:
    BUS_CAPACITY = 25

    def __init__(self, id: int) -> None:
        self.id = id
        self.passenger_requests: List[PassengerRequest] = []
        self.upcoming_stops: List[Stop] = []
        self.time_to_next_stop: int = 0
        self.current_location: Stop = None