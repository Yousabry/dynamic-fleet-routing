import math
from c_types.Stop import Stop
from control.DistanceControl import DistanceControl
from control.config import ACCEPTABLE_TRAVEL_DELAY_PERCENT, ACCEPTABLE_WAIT_FOR_PICKUP_SEC

class PassengerRequest:
    def __init__(self, id: int, start_location: Stop, destination: Stop, request_time: int, dc: DistanceControl) -> None:
        self.id: int = id
        self.start_location: Stop = start_location
        self.destination: Stop = destination
        self.request_time: int = request_time
        self.pickup_time: int = None
        self.arrival_time: int = None
        self.serving_bus_id: int = None
        self.latest_acceptable_pickup: int = request_time + ACCEPTABLE_WAIT_FOR_PICKUP_SEC

        travel_time = dc.get_travel_time_seconds(start_location, destination)
        max_acceptable_travel_time = math.ceil(travel_time * ACCEPTABLE_TRAVEL_DELAY_PERCENT)
        self.latest_acceptable_arrival: int = self.latest_acceptable_pickup + max_acceptable_travel_time

    def __str__(self) -> str:
        return f"{self.id}: {self.start_location} -> {self.destination} (requested {self.request_time})"