from typing import Callable, List
from c_types.Bus import Bus
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from util.compliance import does_bus_satisfy_requests
from util.debug import debug_log

# This heuristic will only consider busses that are within 4km from pickup spot
MAX_DISTANCE_PICKUP = 2

# This heuristic finds the closest bus to the start location of the request and assigns
# that bus the request if it has space
def heuristic_closest_pickup(fleet_control: FleetControl, distance_control: DistanceControl, current_time: int):
    fleet_control.request_pool = [req for req in fleet_control.request_pool if req.latest_acceptable_pickup > current_time]
    request_pool = fleet_control.request_pool.copy()

    if len(request_pool) > 50:
        debug_log(f"{len(request_pool)} requests to check in CP")

    # TODO: quick way to filter out very far busses without called gettraveldistancecoord (which is expensive)

    for req in request_pool:
        distance_calc: Callable[[Bus], Bus] = lambda bus: distance_control.get_travel_distance_coord(bus.current_location, req.start_location.coordinates)
        closest_busses: List[Bus] = [bus for bus in fleet_control.busses if distance_calc(bus) <= MAX_DISTANCE_PICKUP]

        for bus in closest_busses:
            old_path = bus.path.get_copy()

            bus.add_stop_at_index(0, req.start_location, req)
            bus.append_after_stop(req.destination, req, req.start_location)

            if does_bus_satisfy_requests(current_time, bus, distance_control):
                debug_log(f"bus {bus.id} assigned trip request {req.id}")
                fleet_control.request_pool.remove(req)
                break

            else:
                debug_log(f"bus {bus.id} is close but could not be assigned trip request {req.id}")

                bus.path = old_path
                bus.passenger_requests.remove(req)
