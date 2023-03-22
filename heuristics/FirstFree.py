from typing import Callable, List
from c_types.Bus import Bus
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from util.compliance import does_bus_satisfy_requests
from util.debug import debug_log

# This heuristic makes the buses take requests in order. The bus that can arrive the earliest
# at the start location of the new stop after servicing all current requests gets assigned this
# new request at the end of the queue
def heuristic_first_free(fleet_control: FleetControl, distance_control: DistanceControl, current_time: int):
    # for each new request, we assign immediately
    for req in reversed(fleet_control.request_pool):
        distance_calc: Callable[[Bus], Bus] = lambda bus: fleet_control.time_to_arrive_for_pickup(bus, req.start_location, distance_control)
        closest_busses: List[Bus] = fleet_control.busses.copy()
        closest_busses.sort(key=distance_calc)

        # Try busses until we find one that can take it
        for bus in closest_busses:
            old_path = bus.path.get_copy()
            bus.append_request_to_path(req)

            if does_bus_satisfy_requests(current_time, bus, distance_control):
                debug_log(f"bus {bus.id} assigned trip request {req.id}")
                fleet_control.request_pool.pop()
                break

            else:
                debug_log(f"bus {bus.id} is first free but could not be assigned trip request {req.id}")

                bus.path = old_path
                bus.passenger_requests.remove(req)
