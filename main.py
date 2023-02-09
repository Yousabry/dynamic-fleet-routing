import random
from control.CrowdControl import CrowdControl
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from control.config import BATCH_PERIOD_SEC, NUM_SECONDS_IN_DAY
from heuristics.Heuristics import HeuristicEnums, Heuristics

random.seed(666)

def run_analytics(crowd_control: CrowdControl, fleet_control: FleetControl):
    num_requests = len(crowd_control.passenger_requests)

    print("-"*30)
    print(f"Simulation on {num_requests} requests with {len(fleet_control.busses)} busses in the fleet.")

    fulfilled_requests = [r for r in crowd_control.passenger_requests if r.pickup_time]
    total_time_waiting = sum([r.pickup_time - r.request_time for r in fulfilled_requests])
    print(f"{len(fulfilled_requests)}/{num_requests} fulfilled requests")
    avg_wait = -1 if not fulfilled_requests else total_time_waiting/len(fulfilled_requests)
    print(f"Average wait time: {avg_wait} sec")

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
            bus.on_time_tic(current_time)
        
        current_time += BATCH_PERIOD_SEC
        busses_still_working = [bus for bus in busses_still_working if bus.passenger_requests]

    run_analytics(crowd_control, fleet_control)


if __name__ == "__main__":
    simulate_full_day(HeuristicEnums.FIRST_FREE)
    