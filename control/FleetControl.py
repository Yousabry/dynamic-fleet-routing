import random
from typing import List
from c_types.Bus import Bus
from c_types.Request import PassengerRequest
from c_types.Stop import Stop
from control.DistanceControl import DistanceControl
from control.config import FLEET_SIZE


class FleetControl:
    def __init__(self, all_stops: List[Stop]) -> None:
        self.request_pool: List[PassengerRequest] = []
        self.busses: List[Bus] = [Bus(i) for i in range(FLEET_SIZE)]

        for bus in self.busses:
            bus.current_location = random.choice(all_stops).coordinates

    def first_free_bus_to_location(self, stop: Stop, dc: DistanceControl) -> Bus:
        closest_bus = (self.busses[0], self.time_to_arrive_after_path(self.busses[0], stop, dc))

        for i in range(1, len(self.busses)):
            d = self.time_to_arrive_after_path(self.busses[i], stop, dc)
            if d < closest_bus[1]:
                closest_bus = (self.busses[i], d)
        
        return closest_bus[0]

    def time_to_arrive_for_pickup(self, bus: Bus, destination: Stop, distance_control: DistanceControl) -> int:
        if not bus.path:
            return distance_control.get_travel_time_seconds_coord(bus.current_location, destination.coordinates)

        arrival_times = bus.path.get_arrival_times(bus.current_location, distance_control)

        if destination in bus.path:
            return arrival_times[bus.path.index(destination)]
        
        return distance_control.get_travel_time_seconds(bus.path[-1], destination) + arrival_times[-1]

    def time_to_arrive_after_path(self, bus: Bus, destination: Stop, distance_control: DistanceControl) -> int:
        if not bus.path:
            return distance_control.get_travel_time_seconds_coord(bus.current_location, destination.coordinates)

        arrival_times = bus.path.get_arrival_times(bus.current_location, distance_control)
        
        return distance_control.get_travel_time_seconds(bus.path[-1], destination) + arrival_times[-1]