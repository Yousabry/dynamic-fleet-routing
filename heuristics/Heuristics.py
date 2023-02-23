from typing import Callable
from enum import Enum
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from heuristics.ClosestPickup import heuristic_closest_pickup
from heuristics.FirstFree import heuristic_first_free
from heuristics.GroupClose import heuristic_group_close
from heuristics.OneBus import heuristic_one_bus

class HeuristicEnums(Enum):
    CLOSEST_PICKUP = 0
    FIRST_FREE = 1
    GROUP_CLOSE = 2
    WALLER_LP = 3
    ONE_BUS = 4

class Heuristics:
    heuristic_funcs: dict[HeuristicEnums: Callable[[FleetControl, DistanceControl, int], None]] = {
        HeuristicEnums.CLOSEST_PICKUP: heuristic_closest_pickup,
        HeuristicEnums.FIRST_FREE: heuristic_first_free,
        HeuristicEnums.GROUP_CLOSE: heuristic_group_close,
        HeuristicEnums.ONE_BUS: heuristic_one_bus,
    }
