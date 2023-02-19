from c_types.Stop import Stop
from control.config import ACCEPTABLE_WAIT_FOR_PICKUP_SEC

class PassengerRequest:
    def __init__(self, id: int, start_location: Stop, destination: Stop, request_time: int) -> None:
        self.id: int = id
        self.start_location: Stop = start_location
        self.destination: Stop = destination
        self.request_time: int = request_time
        self.pickup_time: int = None
        self.arrival_time: int = None
        self.serving_bus_id: int = None
        self.latest_acceptable_pickup: int = request_time + ACCEPTABLE_WAIT_FOR_PICKUP_SEC
        self.latest_acceptable_arrival: int = 99999999999 # TODO: use tranvel time + buffer

    def __str__(self) -> str:
        return f"{self.id}: {self.start_location} -> {self.destination} (requested {self.request_time})"