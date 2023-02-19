from typing import Callable
from c_types.Bus import Bus
from c_types.Path import Path
from c_types.Request import PassengerRequest
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from util.compliance import do_stops_satisfy_requests
import copy

# This heuristic tries to find requests that are close (can be serviced by the same bus without much inconvenience)
# It creates a path with as many of these requests as possible, then assigns the Path to a bus that can service it in time
def heuristic_group_close(fleet_control: FleetControl, dc: DistanceControl):
    request_pool = fleet_control.request_pool.copy()

    while request_pool:
        path = Path()
        first_req: PassengerRequest = request_pool[0]
        requests_for_path = set()
        bus: Bus = fleet_control.first_free_bus_to_location(first_req.start_location, dc)

        requests_for_path.add(first_req)
        path.append_stop(first_req.start_location)
        path.append_stop(first_req.destination)

        # if this does not work, then we cannot service this req
        if not do_stops_satisfy_requests(bus.current_location, bus.current_passenger_count, bus.path + path, requests_for_path, dc):
            continue

        # sort requests in pool by distance from first_req
        distance_calc: Callable[[PassengerRequest], Bus] = lambda req: dc.get_travel_distance_km(first_req.start_location, req.start_location)
        request_pool.sort(key=distance_calc)

        for req in request_pool:
            # try adding to path see if we can still service this path
            alt_path = copy.copy(path)

            alt_path.add_stop_to_minimize_detour(req.start_location, dc)
            alt_path.append_stop_after_pred(req.destination, req.start_location)
            alt_reqs = requests_for_path
            alt_reqs.add(req)

            if do_stops_satisfy_requests(bus.current_location, bus.current_passenger_count, bus.path + alt_path, alt_reqs, dc):
                requests_for_path.add(req)
                path = alt_path
            
            else:
                break

        for req_added in requests_for_path:
            request_pool.remove(req_added)
        
        # assign path (and all requests in the path) to the closest bus
        bus.path += path
        bus.passenger_requests.update(requests_for_path)

    fleet_control.request_pool.clear()