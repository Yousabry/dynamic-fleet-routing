from control.CrowdControl import CrowdControl
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from heuristics.Heuristics import HeuristicEnums


def simulate_full_day(heuristic: HeuristicEnums):
    distance_control = DistanceControl()
    crowd_control = CrowdControl(distance_control.get_all_stops())
    fleet_control = FleetControl(distance_control.get_all_stops())

    fleet_control.begin_simulation()


if __name__ == "__main__":
    simulate_full_day(HeuristicEnums.CLOSEST_PICKUP)
    