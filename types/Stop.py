class Stop:
    HIGH_TRAFFIC_STOPS = ["7175","6790","7367","1249","2997","8783"]

    def __init__(self, id: str, main_street: str, cross_street: str) -> None:
        self.id: str = id
        self.main_street: str = main_street
        self.cross_street: str = cross_street
        self.high_traffic_stop: bool = id in Stop.HIGH_TRAFFIC_STOPS

    def __str__(self):
        return f"{self.main_street} / {self.cross_street} ({self.id})"