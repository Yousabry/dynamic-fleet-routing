

from typing import Set
from c_types.Path import Path
from c_types.Request import PassengerRequest
from control.DistanceControl import DistanceControl
from control.config import BUS_CAPACITY
from util.debug import debug_log

# This checks the following compliance requirements are followed:
#   - latest_pickup and latest_dropoff are respected for all requests on this bus
#   - the bus is never over capacity

def do_stops_satisfy_requests(current_time: int, bus_current_location: tuple[float, float], bus_current_passenger_count: int, planned_path: Path, requests: Set[PassengerRequest], dc: DistanceControl) -> bool:
    if not planned_path or not requests:
        raise Exception("What am I supposed to do here...")
    
    arrival_times = planned_path.get_arrival_times(bus_current_location, dc)
    capacity_change = [0] * len(arrival_times)
    # check that all requests are satisfied in time
    try:
        for req in requests:
            if not req.pickup_time:
                # validate pickup time
                pickup_stop_idx = planned_path.index(req.start_location)
                planned_pickup_time = current_time + arrival_times[pickup_stop_idx]
                if planned_pickup_time > req.latest_acceptable_pickup:
                    return False

                capacity_change[pickup_stop_idx] += 1
            
            if not req.arrival_time:
                # validate arrival time
                pickup_stop_idx = 0 if req.pickup_time else planned_path.index(req.start_location)
                dest_stop_idx = planned_path.stops[pickup_stop_idx:].index(req.destination)
                planned_arrival_time = current_time + arrival_times[dest_stop_idx]
                if planned_arrival_time > req.latest_acceptable_arrival:
                    return False
                
                capacity_change[dest_stop_idx] -= 1

    except Exception as e:
        print(e)
        return False

    capacities = [bus_current_passenger_count + capacity_change[0]]
    for i in range(1, len(capacity_change)):
        capacities.append(capacities[i-1] + capacity_change[i])

    # validate that capacity is never exceeded
    if max(capacities) > BUS_CAPACITY:
        debug_log(f"Cannot do this plan because bus would be over capacity.")
        return False

    return True