

from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl

# This heuristic finds the closest bus to the start location of the request and assigns
# that bus the request
def heuristic_closest_pickup(fleet_control: FleetControl, distance_control: DistanceControl):
    # for each new request, we assign immediately
    for req in fleet_control.request_pool:
        # find the bus that is closest
        closest_bus = (fleet_control.busses[0], 999999999)

        for bus in fleet_control.busses:
            bus_next_location = bus.upcoming_stops[0] if bus.upcoming_stops else bus.current_location
            distance_from_stop = bus.time_to_next_stop + \
                distance_control.get_distance(bus_next_location, req.start_location)

            if distance_from_stop < closest_bus[1]:
                closest_bus = (bus, distance_from_stop)

        # assign this bus the new request
        bus.upcoming_stops = [req.start_location] + [bus.upcoming_stops] + [req.destination]
