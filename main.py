import random
from typing import List
import networkx as nx

from util.cleanup import build_nx_graph

random.seed(666)
NUM_SECONDS_IN_DAY = 86400

class Stop:
    def __init__(self, id: str, main_street: str, cross_street: str) -> None:
        self.id = id
        self.main_street = main_street
        self.cross_street = cross_street

    def __str__(self):
        return f"{self.main_street} / {self.cross_street} ({self.id})"

class Bus:
    BUS_CAPACITY = 60

    def __init__(self, id: int) -> None:
        self.id = id
        self.current_passenger_count = 0
        self.upcoming_stops = []
        self.time_to_next_stop = 0
        self.current_location = None

class PassengerRequest:
    def __init__(self, id: int, start_location: Stop, destination: Stop, request_time: int) -> None:
        self.id: int = id
        self.start_location: Stop = start_location
        self.destination: Stop = destination
        self.request_time: int = request_time

class CrowdControl:
    NUM_REQUESTS = 100 # 300_000

    def __init__(self) -> None:
        self.passenger_requests: List[PassengerRequest] = []

    def prepare_requests(self, all_stops: List[Stop]) -> None:
        for i in range(CrowdControl.NUM_REQUESTS):
            # TODO: add weight for high volume stops and high volume times
            [start_location, destination] = random.sample(all_stops, 2)
            request_time = random.randint(0, NUM_SECONDS_IN_DAY)

            self.passenger_requests.append(PassengerRequest(i, start_location, destination, request_time))
        
        self.passenger_requests = sorted(self.passenger_requests, key=lambda req: req.request_time)

    def pop_new_requests(self, time: int) -> List[PassengerRequest]:
        new_requests = []

        while len(self.passenger_requests) > 0 and self.passenger_requests[0].request_time <= time:
            new_requests.append(self.passenger_requests.pop(0))

        return new_requests

class FleetControl:
    FLEET_SIZE = 900

    def __init__(self) -> None:
        self.busses: List[Bus] = [Bus(i) for i in range(FleetControl.FLEET_SIZE)]

class DistanceControl:
    def __init__(self) -> None:
        self.nx_graph: nx.Graph = build_nx_graph()

    def get_distance(self, origin: Stop, dest: Stop) -> int:
        return nx.shortest_path_length(self.nx_graph, origin.id, dest.id, weight="distance")

    def find_shortest_path(self, origin: Stop, dest: Stop) -> int:
        return nx.shortest_path(self.nx_graph, origin.id, dest.id, weight="distance")

if __name__ == "__main__":
    crowd_control = CrowdControl()
    distance_control = DistanceControl()
    fleet_control = FleetControl()

    stops = [Stop(node_id, f"main st stop {node_dict['main_street']}", f"cross st stop {node_dict['cross_street']}") for node_id, node_dict in distance_control.nx_graph.nodes.items()]
    crowd_control.prepare_requests(stops)

    # begin simulation
    for time in range(NUM_SECONDS_IN_DAY):
        new_requests = crowd_control.pop_new_requests(time)

        for req in new_requests:
            print(f"Request time {req.request_time} from {req.start_location.id} to --> {req.destination.id} (takes {distance_control.get_distance(req.start_location,req.destination)} min straight)")

