from c_types.Stop import Stop

class PassengerRequest:
    def __init__(self, id: int, start_location: Stop, destination: Stop, request_time: int) -> None:
        self.id: int = id
        self.start_location: Stop = start_location
        self.destination: Stop = destination
        self.request_time: int = request_time
        self.pickup_time: int = None
        self.arrival_time: int = None
        self.latest_acceptable_pickup: int = request_time + 600 # 10 minutes