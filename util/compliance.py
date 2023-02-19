

from typing import Set
from c_types.Bus import Bus
from c_types.Path import Path
from c_types.Request import PassengerRequest
from control.DistanceControl import DistanceControl
from control.config import BUS_CAPACITY
from util.debug import debug_log

# This checks the following compliance requirements are followed:
#   - latest_pickup and latest_dropoff are respected for all requests on this bus
#   - the bus is never over capacity

# THIS DOES NOT LOOK AT BUS CURRENT PATH, IT ASSUMES IT IS EMPTY AND PLANNED_PATH IS THE PATH THE BUS TAKES NOW
def do_stops_satisfy_requests(bus: Bus, planned_path: Path, requests: Set[PassengerRequest], dc: DistanceControl) -> bool:
    if not planned_path or not requests:
        raise Exception("What am I supposed to do here...")
    
    arrival_times = planned_path.get_arrival_times(bus.current_location, dc)
    capacities = [bus.get_current_passenger_count()] * len(arrival_times)
    # check that all requests are satisfied in time
    try:
        for req in requests:
            if not req.pickup_time:
                # validate pickup time
                pickup_stop_idx = planned_path.index(req.start_location)
                planned_pickup_time = arrival_times[pickup_stop_idx]
                if planned_pickup_time > req.latest_acceptable_pickup:
                    return False

                capacities[pickup_stop_idx] += 1
            
            if not req.arrival_time:
                # validate arrival time
                pickup_stop_idx = 0 if req.pickup_time else planned_path.index(req.start_location)
                dest_stop_idx = planned_path.stops[pickup_stop_idx:].index(req.destination)
                planned_arrival_time = arrival_times[dest_stop_idx]
                if planned_arrival_time > req.latest_acceptable_arrival:
                    return False
                
                capacities[dest_stop_idx] -= 1

    except Exception as e:
        print(e)
        # debug_log(e)
        return False

    # validate that capacity is never exceeded
    if max(capacities) > BUS_CAPACITY:
        debug_log(f"Cannot do this plan because bus {bus.id} would be over capacity.")
        return False

    return True