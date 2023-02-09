from typing import Callable, List
from c_types.Bus import Bus
from c_types.Stop import Stop
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from util.compliance import do_stops_satisfy_requests
from util.debug import debug_log

# This heuristic makes the buses take requests in order. The bus that can arrive the earliest
# at the start location of the new stop after servicing all current requests gets assigned this
# new request at the end of the queue
def heuristic_first_free(fleet_control: FleetControl, distance_control: DistanceControl):
    # for each new request, we assign immediately
    for req in fleet_control.request_pool:
        distance_calc: Callable[[Bus], Bus] = lambda bus: time_to_arrive_for_pickup(bus, req.start_location, distance_control)
        closest_busses: List[Bus] = fleet_control.busses.copy()
        closest_busses.sort(key=distance_calc)

        # Try busses until we find one that can take it
        for bus in closest_busses:
            potential_stops = bus.upcoming_stops.copy()
            # TODO: this is not perfect because we are not using append_if_not_already_in_upcoming which has some optimizations
            potential_stops.append(req.start_location)
            potential_stops.append(req.destination)
            potential_reqs = [r for r in bus.passenger_requests.copy()]
            potential_reqs.append(req)

            if do_stops_satisfy_requests(bus, potential_stops, potential_reqs, distance_control):
                debug_log(f"bus {bus.id} assigned trip request {req.id}")

                bus.append_if_not_already_in_upcoming(req.start_location, req)
                bus.append_after_stop(req.destination, req, req.start_location)

                break

            else:
                debug_log(f"bus {bus.id} is first free but could not be assigned trip request {req.id}")

    fleet_control.request_pool.clear()

def time_to_arrive_for_pickup(bus: Bus, destination: Stop, distance_control: DistanceControl) -> int:
    if not bus.upcoming_stops:
        return distance_control.get_travel_time_seconds_coord(bus.current_location, destination.coordinates)

    total_time = distance_control.get_travel_time_seconds_coord(bus.current_location, bus.upcoming_stops[0].coordinates)
    for i in range(1, len(bus.upcoming_stops)):
        # Stop is already in upcoming for this bus
        if bus.upcoming_stops[i-1] == destination:
            return total_time

        total_time += distance_control.get_travel_time_seconds(bus.upcoming_stops[i-1], bus.upcoming_stops[i])

    total_time += distance_control.get_travel_time_seconds(bus.upcoming_stops[-1], destination)

    return total_time