from control.CrowdControl import CrowdControl
from control.FleetControl import FleetControl
import collections

def run_analytics(crowd_control: CrowdControl, fleet_control: FleetControl):
    num_requests = len(crowd_control.passenger_requests)

    print("-"*30)
    print(f"Simulation on {num_requests} requests with {len(fleet_control.busses)} busses in the fleet.")

    fulfilled_requests = [r for r in crowd_control.passenger_requests if r.pickup_time]
    total_time_waiting = sum([r.pickup_time - r.request_time for r in fulfilled_requests])
    total_travel_time = sum([r.arrival_time - r.pickup_time for r in fulfilled_requests])
    print(f"{len(fulfilled_requests)}/{num_requests} fulfilled requests")
    avg_wait = -1 if not fulfilled_requests else total_time_waiting/len(fulfilled_requests)
    avg_travel = -1 if not fulfilled_requests else total_travel_time/len(fulfilled_requests)

    print(f"Average wait time:   {avg_wait} sec")
    print(f"Average travel time: {avg_travel} sec")
    print("-"*30)

    # Each bus and the number of requests they served
    serving_busses = []
    for req in crowd_control.passenger_requests:
        serving_busses.append(req.serving_bus_id)

    ctr = collections.Counter(serving_busses)
    print(ctr)

    # Each bus and the path they took
    for bus in fleet_control.busses:
        stops = [s.coordinates for s in bus.stops_visited]
        bus_reqs = []
        print(f"Bus {bus.id} went to stops: {stops}")

        for req in crowd_control.passenger_requests:
            if req.serving_bus_id == bus.id:
                bus_reqs.append([req.start_location.coordinates, req.destination.coordinates])
        
        print(f"Bus {bus.id} reqs: {bus_reqs}")