from control.config import HIGH_TRAFFIC_STOPS

class Stop:
    def __init__(self, stop_id: str, stop_code: str, stop_name: str, coordinates: tuple[float, float]) -> None:
        self.stop_id: str = stop_id
        self.stop_code: str = stop_code
        self.stop_name: str = stop_name
        self.high_traffic_stop: bool = stop_code in HIGH_TRAFFIC_STOPS
        self.coordinates: tuple[float, float] = coordinates

    def __str__(self):
        return f"{self.stop_name} ({self.stop_id})"