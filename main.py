import random
from control.CrowdControl import CrowdControl
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from control.config import BATCH_PERIOD_SEC, NUM_SECONDS_IN_DAY
from heuristics.Heuristics import HeuristicEnums, Heuristics
from util.debug import debug_log
import time

random.seed(6666)

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
    print(f"Average wait time: {avg_wait} sec")
    print(f"Average travel time: {avg_travel} sec")
    print("-"*30)

def simulate_full_day(heuristic: HeuristicEnums):
    print(f"Running simulation with {heuristic} heuristic.")

    distance_control = DistanceControl()
    crowd_control = CrowdControl(distance_control.all_stops)
    fleet_control = FleetControl(distance_control.all_stops)
    time_start = time.time()

    # begin simulation
    current_time = 0
    while current_time <= NUM_SECONDS_IN_DAY:
        debug_log(f"Current simulation time: {current_time}")
        current_time += BATCH_PERIOD_SEC

        for bus in fleet_control.busses:
            bus.on_time_tic(current_time, distance_control)

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
            bus.on_time_tic(current_time, distance_control)
        
        current_time += BATCH_PERIOD_SEC
        busses_still_working = [bus for bus in busses_still_working if bus.passenger_requests]

    time_end = time.time()
    print(f"Simulation took {time_end-time_start} seconds to complete.")
    run_analytics(crowd_control, fleet_control)


if __name__ == "__main__":
    simulate_full_day(HeuristicEnums.ONE_BUS)
    