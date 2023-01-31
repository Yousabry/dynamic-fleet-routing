import random
from control.CrowdControl import CrowdControl
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from control.config import BATCH_PERIOD_SEC, NUM_SECONDS_IN_DAY
from heuristics.Heuristics import HeuristicEnums, Heuristics

random.seed(666)

def run_analytics(crowd_control: CrowdControl, fleet_control: FleetControl):
    num_requests = len(crowd_control.passenger_requests)

    print(f"Simulation on {num_requests} requests with {len(fleet_control.busses)} busses in the fleet.")

    total_time_waiting = sum([r.pickup_time - r.request_time for r in crowd_control.passenger_requests])
    print(f"Average wait time: {total_time_waiting/num_requests}")

    # for req in new_requests:
    #     print(f" time {req.request_time} from {req.start_location.id} to --> {req.destination.id} (takes {distance_control.get_distance(req.start_location,req.destination)} min straight)")

def simulate_full_day(heuristic: HeuristicEnums):
    print(f"Running simulation with {heuristic} heuristic.")

    distance_control = DistanceControl()
    crowd_control = CrowdControl(distance_control.all_stops)
    fleet_control = FleetControl(distance_control.all_stops)

    # begin simulation
    current_time = 0
    while current_time <= NUM_SECONDS_IN_DAY:
        current_time += BATCH_PERIOD_SEC

        for bus in fleet_control.busses:
            bus.on_time_tic(current_time)

        # Handle new requests by batch
        new_requests = crowd_control.pop_new_requests(current_time)
        fleet_control.request_pool += new_requests

        # Let heuristic manage fleet and requests
        Heuristics.heuristic_funcs[heuristic](fleet_control, distance_control)

    # run out clock to let last passengers arrive
    current_time = NUM_SECONDS_IN_DAY + 1
    busses_still_working = [bus for bus in fleet_control.busses if bus.passenger_requests]
    while busses_still_working:
        for bus in busses_still_working:
            bus.on_time_tic()
        
        current_time += 1
        busses_still_working = [bus for bus in busses_still_working if bus.passenger_requests]

    run_analytics(crowd_control, fleet_control)


if __name__ == "__main__":
    simulate_full_day(HeuristicEnums.CLOSEST_PICKUP)
    