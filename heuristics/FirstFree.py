from c_types.Bus import Bus
from c_types.Stop import Stop
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl

# This heuristic makes the buses take requests in order. The bus that can arrive the earliest
# at the start location of the new stop after servicing all current requests gets assigned this
# new request at the end of the queue
def heuristic_first_free(fleet_control: FleetControl, distance_control: DistanceControl):
    # for each new request, we assign immediately
    for req in fleet_control.request_pool:
        # find the bus that will be able to reach the stop the earliest
        closest_bus = (fleet_control.busses[0], 9999999)
        
        for bus in fleet_control.busses:
            bus_can_arrive_by = time_to_arrive_for_pickup(bus, req.start_location, distance_control)

            if bus_can_arrive_by < closest_bus[1]:
                closest_bus = (bus, bus_can_arrive_by)
        
        # assign this bus the new request
        bus = closest_bus[0]
        bus.append_if_not_already_in_upcoming(req.start_location, req)
        bus.append_after_stop(req.destination, req, req.start_location)

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