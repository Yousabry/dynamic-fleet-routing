from typing import Callable, List
from c_types.Bus import Bus
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from util.compliance import do_stops_satisfy_requests
from util.debug import debug_log
import copy

# This heuristic finds the closest bus to the start location of the request and assigns
# that bus the request if it has space
def heuristic_closest_pickup(fleet_control: FleetControl, distance_control: DistanceControl):
    # for each new request, we assign immediately
    for req in fleet_control.request_pool:
        distance_calc: Callable[[Bus], Bus] = lambda bus: distance_control.get_travel_distance_coord(bus.current_location, req.start_location.coordinates)
        closest_busses: List[Bus] = fleet_control.busses.copy()
        closest_busses.sort(key=distance_calc)

        for bus in closest_busses:
            potential_path = copy.copy(bus.path)
            potential_path.add_stop_at_index(1, req.start_location)
            potential_path.append_stop(req.destination)
            potential_reqs = bus.passenger_requests.copy()
            potential_reqs.add(req)

            if do_stops_satisfy_requests(bus, potential_path, potential_reqs, distance_control):
                debug_log(f"bus {bus.id} assigned trip request {req.id}")

                bus.add_stop_at_index(1, req.start_location, req)        
                bus.append_after_stop(req.destination, req, req.start_location)

                break

            else:
                debug_log(f"bus {bus.id} is close but could not be assigned trip request {req.id}")

    fleet_control.request_pool.clear()