from typing import Callable
from c_types.Bus import Bus
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl

# This heuristic finds the closest bus to the start location of the request and assigns
# that bus the request if it has space
def heuristic_closest_pickup(fleet_control: FleetControl, distance_control: DistanceControl):
    # for each new request, we assign immediately
    for req in fleet_control.request_pool:
        distance_calc: Callable[[Bus], Bus] = lambda bus: distance_control.get_travel_distance_coord(bus.current_location, req.start_location.coordinates)
        closest_bus: Bus = min(fleet_control.busses, key=distance_calc)

        print(f"bus {closest_bus.id} assigned trip request {req.id}")

        if closest_bus.upcoming_stops:
            closest_bus.add_stop_at_index(1, req.start_location, req)
            closest_bus.append_stop_to_upcoming(req.destination, req)
        else:
            closest_bus.append_stop_to_upcoming(req.start_location, req)
            closest_bus.append_stop_to_upcoming(req.destination, req)

    fleet_control.request_pool.clear()