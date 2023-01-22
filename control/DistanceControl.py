from typing import List
import networkx as nx
from c_types.Stop import Stop

from util.cleanup import build_nx_graph


class DistanceControl:
    GRAPH_WEIGHT_LABEL = "distance"

    def __init__(self) -> None:
        self.nx_graph: nx.Graph = build_nx_graph()
        self.all_stops: List[Stop] = []

        for node_id, node_dict in self.nx_graph.nodes.items():
            self.all_stops.append(Stop(node_id, f"main st stop {node_dict['main_street']}", f"cross st stop {node_dict['cross_street']}"))
    
    def get_all_stops(self) -> List[Stop]:
        return self.all_stops

    def get_distance(self, origin: Stop, dest: Stop) -> int:
        return nx.shortest_path_length(self.nx_graph, origin.id, dest.id, weight=DistanceControl.GRAPH_WEIGHT_LABEL)

    def find_shortest_path(self, origin: Stop, dest: Stop) -> List[any]:
        return nx.shortest_path(self.nx_graph, origin.id, dest.id, weight=DistanceControl.GRAPH_WEIGHT_LABEL)

    def get_length_of_path(self, path: List[str]) -> int:
        return nx.path_weight(self.nx_graph, path, weight=DistanceControl.GRAPH_WEIGHT_LABEL)