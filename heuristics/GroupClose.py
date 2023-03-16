from typing import Callable
from c_types.Bus import Bus
from c_types.Path import Path
from c_types.Request import PassengerRequest
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from util.compliance import do_stops_satisfy_requests

# This heuristic tries to find requests that are close (can be serviced by the same bus without much inconvenience)
# It creates a path with as many of these requests as possible, then assigns the Path to a bus that can service it in time
def heuristic_group_close(fleet_control: FleetControl, dc: DistanceControl, current_time: int):
    request_pool = fleet_control.request_pool.copy()

    while request_pool:
        first_req: PassengerRequest = request_pool[0]
        (bus, time_to_arrive) = fleet_control.first_free_bus_to_location(first_req.start_location, dc)
        arrival_time = current_time + time_to_arrive

        # if this does not work, then we cannot service this req
        if arrival_time > first_req.latest_acceptable_pickup:
            request_pool.pop(0)
            continue

        path, requests_for_path = Path(), set()
        requests_for_path.add(first_req)
        path.append_stop(first_req.start_location)
        path.append_stop(first_req.destination)

        # sort requests in pool by distance from first_req
        distance_calc: Callable[[PassengerRequest], Bus] = lambda req: dc.get_travel_distance_km(first_req.start_location, req.start_location)
        request_pool.sort(key=distance_calc)

        for req in request_pool:
            # try adding to path see if we can still service this path
            alt_path = path.get_copy()

            alt_path.add_stop_to_minimize_detour(req.start_location, dc)
            alt_path.append_stop_after_pred(req.destination, req.start_location)
            alt_reqs = requests_for_path.copy()
            alt_reqs.add(req)

            if do_stops_satisfy_requests(current_time, bus.current_location, bus.current_passenger_count, bus.path + alt_path, alt_reqs, dc):
                requests_for_path.add(req)
                path = alt_path
            
            else:
                break

        for req_added in requests_for_path:
            request_pool.remove(req_added)
            fleet_control.request_pool.remove(req_added)
        
        # assign path (and all requests in the path) to the closest bus
        bus.path += path
        bus.passenger_requests.update(requests_for_path)

    # remove requests that have expired
    fleet_control.request_pool = [r for r in fleet_control.request_pool if r.latest_acceptable_pickup > current_time]