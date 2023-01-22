from control.CrowdControl import CrowdControl
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from heuristics.Heuristics import HeuristicEnums, Heuristics

NUM_SECONDS_IN_DAY = 86400

def run_analytics(crowd_control: CrowdControl, fleet_control: FleetControl):
    num_requests = len(crowd_control.passenger_requests)

    print(f"Simulation on {num_requests} with {len(fleet_control.busses)} busses in the fleet.")

    total_time_waiting = sum([r.pickup_time - r.request_time for r in crowd_control.passenger_requests])
    print(f"Average wait time: {total_time_waiting/num_requests}")

    # for req in new_requests:
    #     print(f" time {req.request_time} from {req.start_location.id} to --> {req.destination.id} (takes {distance_control.get_distance(req.start_location,req.destination)} min straight)")

def simulate_full_day(heuristic: HeuristicEnums):
    print(f"Running simulation with {heuristic} heuristic.")

    distance_control = DistanceControl()
    crowd_control = CrowdControl(distance_control.get_all_stops())
    fleet_control = FleetControl(distance_control.get_all_stops())

    # begin simulation
    for time in range(0, NUM_SECONDS_IN_DAY+1):
        for bus in fleet_control.busses:
            bus.on_time_tic(time, distance_control)

        if time % FleetControl.BATCH_PERIOD_SEC == 0:
            new_requests = crowd_control.pop_new_requests(time)

            # Handle new requests by batch
            fleet_control.request_pool += new_requests

            # Let heuristic manage fleet and requests
            Heuristics.heuristic_funcs[heuristic](fleet_control, distance_control)

    run_analytics(crowd_control, fleet_control)

if __name__ == "__main__":
    simulate_full_day(HeuristicEnums.CLOSEST_PICKUP)
    