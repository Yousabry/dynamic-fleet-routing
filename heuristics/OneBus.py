from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from util.compliance import do_stops_satisfy_requests, does_bus_satisfy_requests

# This heuristic assigns all requests to the first bus
def heuristic_one_bus(fleet_control: FleetControl, dc: DistanceControl, current_time: int):
    bus = fleet_control.busses[0]

    for req in fleet_control.request_pool:
        old_path = bus.path.get_copy()

        bus.append_request_to_path(req)

        if not does_bus_satisfy_requests(current_time,bus, dc):
            bus.path = old_path
            bus.passenger_requests.remove(req)

    fleet_control.request_pool.clear()