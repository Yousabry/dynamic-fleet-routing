from typing import Callable, List
from c_types.Bus import Bus
from c_types.Stop import Stop
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from util.compliance import do_stops_satisfy_requests
from util.debug import debug_log
import copy

# This heuristic makes the buses take requests in order. The bus that can arrive the earliest
# at the start location of the new stop after servicing all current requests gets assigned this
# new request at the end of the queue
def heuristic_first_free(fleet_control: FleetControl, distance_control: DistanceControl):
    # for each new request, we assign immediately
    for req in fleet_control.request_pool:
        distance_calc: Callable[[Bus], Bus] = lambda bus: fleet_control.time_to_arrive_for_pickup(bus, req.start_location, distance_control)
        closest_busses: List[Bus] = fleet_control.busses.copy()
        closest_busses.sort(key=distance_calc)

        # Try busses until we find one that can take it
        for bus in closest_busses:
            potential_path = copy.copy(bus.path)
            potential_path.append_stop_if_not_in_path(req.start_location)
            potential_path.append_stop_after_pred(req.destination, req.start_location)
            potential_reqs = bus.passenger_requests.copy()
            potential_reqs.add(req)

            if do_stops_satisfy_requests(bus.current_location,bus.current_passenger_count, potential_path, potential_reqs, distance_control):
                debug_log(f"bus {bus.id} assigned trip request {req.id}")

                bus.append_if_not_already_in_upcoming(req.start_location, req)
                bus.append_after_stop(req.destination, req, req.start_location)

                break

            else:
                debug_log(f"bus {bus.id} is first free but could not be assigned trip request {req.id}")

    fleet_control.request_pool.clear()
