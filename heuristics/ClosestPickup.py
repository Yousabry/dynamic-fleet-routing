from typing import Callable
from c_types.Bus import Bus
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl

# This heuristic finds the closest bus to the start location of the request and assigns
# that bus the request if it has space
def heuristic_closest_pickup(fleet_control: FleetControl, distance_control: DistanceControl):
    # for each new request, we assign immediately
    for req in fleet_control.request_pool:
        # find the bus that is closest
        # closest_bus = fleet_control.busses[0]
        # closest_bus_distance = distance_control.get_travel_distance_coord(fleet_control.busses[0].current_location, req.start_location.coordinates)

        # for i in range(1, len(fleet_control.busses)):
        #     d = distance_control.get_travel_distance_coord(fleet_control.busses[i].current_location, req.start_location.coordinates)
        #     if d < closest_bus_distance:
        #         closest_bus, closest_bus_distance = fleet_control.busses[i], d

        distance_calc: Callable[[Bus], Bus] = lambda bus: distance_control.get_travel_distance_coord(bus.current_location, req.start_location.coordinates)
        closest_bus: Bus = min(fleet_control.busses, key=distance_calc)

        print(f"bus {closest_bus.id} assigned trip request {req.id}")

        if closest_bus.upcoming_stops:
            closest_bus.upcoming_stops.insert(1, req.start_location)
            closest_bus.upcoming_stops.append(req.destination)
        else:
            closest_bus.upcoming_stops = [req.start_location, req.destination]

    fleet_control.request_pool.clear()