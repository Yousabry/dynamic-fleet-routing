# Used to parse and cleanup edge data from files
# - Converts from text to simple int for edge weight (accounts for walking distances)
# - Verifies no invalid edge weights (anything bigger than 2hr is discarded)

import os
import math
import networkx as nx

DATA_PATH = '../transferred_data/backup_jan19/'
WALK_DRIVE_RATIO = 4 # assume 4 min walk can be driven in 1 min
NUM_EDGE_FILES = 50
script_dir = os.path.dirname(__file__)


def parse_time_minutes(time: str) -> int:
    # Test parser works correctly 
    # print(parse_time_minutes("11 hr 57 min")) #717
    # print(parse_time_minutes("1 hr")) # 60
    # print(parse_time_minutes("23 min")) #23
    # print(parse_time_minutes("15 min walk")) # 3
    
    mins = 0
    fields = time.split()

    if fields[-1] == "walk":
        return math.floor(parse_time_minutes(" ".join(fields[:-1])) / WALK_DRIVE_RATIO)

    # ["1","hr","2","min"]
    for idx in range(0, len(fields)-1):
        if fields[idx+1] in ('min', 'mins', 'minutes'):
            mins += int(fields[idx])
        elif fields[idx+1] in ('hr', 'hrs', 'hours'):
            mins += int(fields[idx]) * 60

    return mins

def build_nx_graph() -> nx.Graph:
    nx_graph = nx.Graph()

    stops_abs_file_path = os.path.join(script_dir, f"{DATA_PATH}/clean_stops.txt")

    with open(stops_abs_file_path, "r") as stops_file:
        for stop in stops_file:
            [s1, s2, stop_id] = stop.strip().split(",")
            nx_graph.add_node(stop_id, main_street=s1, cross_street=s2)

    for a in range(NUM_EDGE_FILES):
        edges_abs_file_path = os.path.join(script_dir, f"{DATA_PATH}/edge_weights{a}.txt")

        if not os.path.isfile(edges_abs_file_path):
            raise Exception(f"could not find file: {edges_abs_file_path}")

        with open(edges_abs_file_path, "r") as edges_file:
            for edge_info in edges_file:
                try:
                    [stop1, stop2, time] = edge_info.strip().split(",")
                    nx_graph.add_edge(stop1, stop2, distance=parse_time_minutes(time))
                    
                except Exception as e:
                    print(f"could not parse line in file {a}: {edge_info}")
                    print(e)

    if len(nx_graph) != 3649:
        raise Exception(f"Size of graph is different than expected! Size is: {len(nx_graph)}")

    return nx_graph
