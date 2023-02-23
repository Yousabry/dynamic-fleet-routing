from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from util.compliance import do_stops_satisfy_requests

# This heuristic assigns all requests to the first bus
def heuristic_one_bus(fleet_control: FleetControl, dc: DistanceControl, current_time: int):
    bus = fleet_control.busses[0]

    for req in fleet_control.request_pool:
        potential_path = bus.path.get_copy()
        potential_path.append_stop_if_not_in_path(req.start_location)
        potential_path.append_stop_after_pred(req.destination, req.start_location)
        potential_reqs = bus.passenger_requests.copy()
        potential_reqs.add(req)

        if do_stops_satisfy_requests(current_time, bus.current_location, bus.current_passenger_count, potential_path, potential_reqs, dc):
            bus.append_if_not_already_in_upcoming(req.start_location, req)
            bus.append_after_stop(req.destination, req, req.start_location)

    fleet_control.request_pool.clear()