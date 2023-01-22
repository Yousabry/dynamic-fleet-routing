from typing import Callable
from enum import Enum
from control.DistanceControl import DistanceControl

from control.FleetControl import FleetControl
from heuristics.ClosestPickup import heuristic_closest_pickup
from heuristics.FirstFree import heuristic_first_free

class HeuristicEnums(Enum):
    CLOSEST_PICKUP = 0
    FIRST_FREE = 1
    WALLER_LP = 2

class Heuristics:
    heuristic_funcs: dict[HeuristicEnums: Callable[[FleetControl, DistanceControl], None]] = {
        HeuristicEnums.CLOSEST_PICKUP: heuristic_closest_pickup,
        HeuristicEnums.FIRST_FREE: heuristic_first_free,
    }
