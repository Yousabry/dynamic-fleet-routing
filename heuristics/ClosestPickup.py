from typing import Callable, Dict, List
from c_types.Bus import Bus
from control.DistanceControl import DistanceControl
from control.FleetControl import FleetControl
from util.compliance import does_bus_satisfy_requests
from util.debug import debug_log
from math import floor

# This heuristic will only consider busses that are within 2km from pickup spot
MAX_DISTANCE_PICKUP = 2

# boundaries of stop coordinates
# min_x, min_y, max_x, max_y = 45.130139, -76.040008, 45.519695, -75.344123

# 2km difference in long/lat
coord_radius = 0.025
def convert_coord_to_segment(coord: tuple[float, float]) -> str:
    return f"{floor(coord[0]/coord_radius)},{floor(coord[1]/coord_radius)}"

def segment_busses(busses: List[Bus]) -> Dict[str, List[Bus]]:
    segments: Dict[str, List[Bus]] = {}

    for bus in busses:
        bus_segment: str = convert_coord_to_segment(bus.current_location)

        if bus_segment not in segments:
            segments[bus_segment] = [bus]
        else:
            segments[bus_segment].append(bus)

    return segments

def get_busses_around_segment(busses_by_segment: Dict[str, List[Bus]], segment: str) -> List[Bus]:
    busses = []
    segment_vals = [int(x) for x in segment.split(",")]

    for lat in range(-1, 2):
        for long in range(-1, 2):
            neighbour_segment = f"{segment_vals[0] + lat},{segment_vals[1] + long}"
            if neighbour_segment in busses_by_segment:
                busses += busses_by_segment.get(neighbour_segment, [])

    return busses

# This heuristic finds the closest bus to the start location of the request and assigns
# that bus the request if it has space
def heuristic_closest_pickup(fleet_control: FleetControl, distance_control: DistanceControl, current_time: int):
    fleet_control.request_pool = [req for req in fleet_control.request_pool if req.latest_acceptable_pickup > current_time]
    request_pool = fleet_control.request_pool.copy()

    busses_by_segment: Dict[str, List[Bus]] = segment_busses(fleet_control.busses)

    for req in request_pool:
        req_segment = convert_coord_to_segment(req.start_location.coordinates)
        busses = get_busses_around_segment(busses_by_segment, req_segment)

        distance_calc: Callable[[Bus], Bus] = lambda bus: distance_control.get_travel_distance_coord(bus.current_location, req.start_location.coordinates)
        closest_busses: List[Bus] = [bus for bus in busses if distance_calc(bus) <= MAX_DISTANCE_PICKUP]

        for bus in closest_busses:
            old_path = bus.path.get_copy()
            bus.add_request_custom_cp(req)

            if does_bus_satisfy_requests(current_time, bus, distance_control):
                debug_log(f"bus {bus.id} assigned trip request {req.id}")
                fleet_control.request_pool.remove(req)
                break

            else:
                debug_log(f"bus {bus.id} is close but could not be assigned trip request {req.id}")

                bus.path = old_path
                bus.passenger_requests.remove(req)
