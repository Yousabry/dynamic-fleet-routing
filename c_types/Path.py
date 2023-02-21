from __future__ import annotations
from typing import List
from c_types.Stop import Stop
from control.DistanceControl import DistanceControl

class Path:
    def __init__(self) -> None:
        self.stops: List[Stop] = []

    def __bool__(self) -> bool:
        return len(self.stops) != 0

    def __len__(self) -> int:
        return len(self.stops)
    
    def __getitem__(self, key: int) -> Stop:
        return self.stops[key]
    
    def __contains__(self, key: Stop) -> bool:
        return key in  self.stops

    def __iadd__(self, other: Path) -> Path:
        for s in other.stops:
            self.append_stop(s)

        return self
    
    def __add__(self, other: Path) -> Path:
        new_path = Path()
        new_path += self
        new_path += other
        return new_path
    
    def index(self, stop: Stop) -> int:
        return self.stops.index(stop)

    def peek_front(self) -> Stop:
        if not self.stops:
            raise Exception("no stops in Path to peek front")

        return self.stops[0]
    
    def pop_front(self) -> Stop:
        if not self.stops:
            raise Exception("no stops in Path to pop")

        return self.stops.pop(0)

    def get_copy(self) -> Path:
        copy_path = Path()
        copy_path.stops = self.stops.copy()
        return copy_path

    def append_stop(self, stop: Stop):
        if not self.stops or self.stops[-1] != stop:
            self.stops.append(stop)

    def append_stops(self, stops: List[Stop]):
        for s in stops:
            self.append_stop(s)

    def append_stop_if_not_in_path(self, stop: Stop):
        if stop in self.stops:
            return
        
        self.append_stop(stop)

    # makes sure that the given stop exists in the path after the first
    # instance of the predecessor
    def append_stop_after_pred(self, stop: Stop, pred: Stop):
        pred_idx = self.stops.index(pred)

        if stop in self.stops[pred_idx:]:
            return
        
        self.append_stop(stop)

    def add_stop_at_index(self, idx: int, stop: Stop):
        if idx >= len(self.stops):
            self.stops.append(stop)
            return
        
        predecessor_idx, successor_idx = idx - 1, idx
        
        # we never want the same stop listed twice consecutively
        if predecessor_idx >= 0 and self.stops[predecessor_idx] == stop:
            return
        
        if successor_idx < len(self.stops) and self.stops[successor_idx] == stop:
            return

        self.stops.insert(idx, stop)

    def add_stop_to_minimize_detour(self, stop: Stop, dc: DistanceControl):
        if len(self.stops) < 2:
            self.stops.append(stop)
            return
        
        best_idx = (1, 99999999)
        
        for i in range(1, len(self.stops)):
            to_stop = dc.get_travel_time_seconds(self.stops[i-1], stop)
            from_stop = dc.get_travel_time_seconds(stop, self.stops[i])
            old_edge = dc.get_travel_time_seconds(self.stops[i-1], self.stops[i])
            distance_added = to_stop + from_stop - old_edge

            if distance_added < best_idx[1]:
                best_idx = (i, distance_added)

        self.add_stop_at_index(best_idx[0], stop)


    # build time to arrival array for all upcoming stops planned
    def get_arrival_times(self, bus_location: tuple[float, float], dc: DistanceControl) -> List[int]:
        if not self.stops:
            return []
        
        arrival_times = []
        arrival_times.append(dc.get_travel_time_seconds_coord(bus_location, self.stops[0].coordinates))

        for i in range(1, len(self.stops)):
            arrival_times.append(dc.get_travel_time_seconds(self.stops[i-1], self.stops[i]) + arrival_times[i-1])

        return arrival_times