from typing import Callable
from enum import Enum
from control.DistanceControl import DistanceControl

from control.FleetControl import FleetControl
from heuristics.ClosestPickup import heuristic_closest_pickup

class HeuristicEnums(Enum):
    CLOSEST_PICKUP = 0
    WALLER_LP = 1

class Heuristics:
    heuristic_funcs: dict[HeuristicEnums: Callable[[FleetControl, DistanceControl], None]] = {
        HeuristicEnums.CLOSEST_PICKUP: heuristic_closest_pickup,
    }
