from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl

# This heuristic finds the closest bus to the start location of the request and assigns
# that bus the request
def heuristic_closest_pickup(fleet_control: FleetControl, distance_control: DistanceControl):
    # for each new request, we assign immediately
    for req in fleet_control.request_pool:
        # find the bus that is closest
        closest_bus_distance_pair = (fleet_control.busses[0], 9999999)

        for bus in fleet_control.busses:
            bus_next_location = bus.upcoming_stops[0] if bus.upcoming_stops else bus.current_location
            distance_from_stop = bus.time_to_next_stop + distance_control.get_distance(bus_next_location, req.start_location)

            if distance_from_stop < closest_bus_distance_pair[1]:
                closest_bus_distance_pair = (bus, distance_from_stop)

        # assign this bus the new request
        closest_bus = closest_bus_distance_pair[0]
        print(f"bus {closest_bus.id} assigned trip request {req.id}")

        if closest_bus.upcoming_stops:
            closest_bus.upcoming_stops.insert(1, req.start_location)
            closest_bus.upcoming_stops.append(req.destination)
        else:
            closest_bus.upcoming_stops = [req.start_location, req.destination]
            closest_bus.time_to_next_stop = distance_control.get_distance(closest_bus.current_location, req.start_location)

    fleet_control.request_pool.clear()