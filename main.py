import random
from tqdm import tqdm
from control.CrowdControl import CrowdControl
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from control.config import BATCH_PERIOD_SEC, NUM_SECONDS_IN_DAY
from heuristics.Heuristics import HeuristicEnums, Heuristics
from util.analytics import run_analytics
from util.debug import debug_log
import time

random.seed(99999)

def simulate_full_day(heuristic: HeuristicEnums):
    print(f"Running simulation with {heuristic} heuristic.")

    distance_control = DistanceControl()
    crowd_control = CrowdControl(distance_control)
    fleet_control = FleetControl(distance_control.all_stops)
    time_start = time.time()

    # begin simulation
    for current_time in tqdm(range(0, NUM_SECONDS_IN_DAY+1, BATCH_PERIOD_SEC), desc="Progress", ascii=False, ncols=75):
        debug_log(f"Current simulation time: {current_time}")

        for bus in fleet_control.busses:
            bus.on_time_tic(current_time, distance_control)

        # Handle new requests by batch
        new_requests = crowd_control.pop_new_requests(current_time)
        fleet_control.request_pool += new_requests

        # Let heuristic manage fleet and requests
        Heuristics.heuristic_funcs[heuristic](fleet_control, distance_control, current_time)

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
    simulate_full_day(HeuristicEnums.CLOSEST_PICKUP)
    