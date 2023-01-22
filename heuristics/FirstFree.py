from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl

# This heuristic makes the buses take requests in order. The bus that can arrive the earliest
# at the start location of the new stop after servicing all current requests gets assigned this
# new request at the end of the queue
def heuristic_first_free(fleet_control: FleetControl, distance_control: DistanceControl):
    # for each new request, we assign immediately
    for req in fleet_control.request_pool:
        # find the bus that will be able to reach the stop the earliest
        closest_bus = (fleet_control.busses[0], 999999999)
        
        for bus in fleet_control.busses:
            bus_can_arrive_by = bus.time_to_next_stop
            
            if len(bus.upcoming_stops) == 0:
                bus_can_arrive_by += distance_control.get_distance(bus.current_location, req.start_location)
            else:
                bus_can_arrive_by += distance_control.get_length_of_path(bus.upcoming_stops) + \
                    distance_control.get_distance(bus.upcoming_stops[-1], req.start_location)

            if bus_can_arrive_by < closest_bus[1]:
                closest_bus = (bus, bus_can_arrive_by)
        
        # assign this bus the new request
        bus.upcoming_stops = [bus.upcoming_stops] + [req.start_location, req.destination]
