# This util takes the edge weights from the scraped txt files, and uses the coordinates to
# create one consolidated list of edges.

import sys
import os
from geopy import distance as geodistance
import networkx as nx
from math import floor
import requests

DATA_PATH = '../data/'
WALK_DRIVE_RATIO = 4 # assume 4 min walk can be driven in 1 min
KM_TO_TIME_MULTIPLE = 1.4 # if geo distance is 10km, travel distance is >= 10 * 1.4 = 14 min

script_dir = os.path.dirname(__file__)
stops_abs_file_path = os.path.join(script_dir, f"{DATA_PATH}/stops.txt")
edges_output_abs_file_path = os.path.join(script_dir, f"{DATA_PATH}/edges.txt")

def parse_time_minutes(time: str) -> int:
    mins = 0
    fields = time.split()

    if fields[-1] == "walk":
        return floor(parse_time_minutes(" ".join(fields[:-1])) / WALK_DRIVE_RATIO)

    # ["1","hr","2","min"]
    for idx in range(0, len(fields)-1):
        if fields[idx+1] in ('min', 'mins', 'minutes'):
            mins += int(fields[idx])
        elif fields[idx+1] in ('hr', 'hrs', 'hours'):
            mins += int(fields[idx]) * 60

    return mins

def send_notif(message, description, type):
    requests.post("https://api.mynotifier.app", {
        "apiKey": 'd3afbf45-1111-4e4e-9d9a-5ec95ac88698',
        "message": message,
        "description": description,
        "project": "68192e",
        "type": type, # info, error, warning or success
    })

def get_already_done_edges():
    already_done = {}
    with open(edges_output_abs_file_path, "r") as edges_file:
        for edge in edges_file:
            [stop1,stop2,distance,path] = edge.strip().split(",")
            already_done[stop1+stop2] = True

    return already_done

def consolidate_edges():
    nx_graph = nx.Graph()
    stops = {}

    with open(stops_abs_file_path, "r") as stops_file:
        stops_file.readline()

        for stop in stops_file:
            [stop_id,stop_code,stop_name,stop_lat,stop_lon] = stop.strip().split(",")
            nx_graph.add_node(stop_code)
            stops[stop_code] = (stop_lat,stop_lon)

    for a in range(50):
        edges_abs_file_path = os.path.join(script_dir, f"{DATA_PATH}/edge_weights{a}.txt")

        if not os.path.isfile(edges_abs_file_path):
            raise Exception(f"could not find file: {edges_abs_file_path}")

        with open(edges_abs_file_path, "r") as edges_file:
            for edge_info in edges_file:
                try:
                    [stop1, stop2, time] = edge_info.strip().split(",")

                    if stop1 not in stops or stop2 not in stops:
                        continue

                    dist_from_scraper = parse_time_minutes(time)
                    dist_from_geo = floor(geodistance.distance(stops[stop1], stops[stop2]).km * KM_TO_TIME_MULTIPLE)

                    dist_final = max(dist_from_scraper, dist_from_geo)

                    nx_graph.add_edge(stop1, stop2, weight=dist_final)
                    
                except Exception as e:
                    print(f"could not parse line in file {a}: {edge_info}")
                    print(e)
    
    # calculate all edge lengths and paths, write to txt
    already_calculated_edges = get_already_done_edges()
    all_stops = list(stops.keys())
    num_stops = len(all_stops)

    s, e = int(sys.argv[1]), int(sys.argv[2]) + 1
    
    for i in range(s, max(e, num_stops - 1)):
        edges_to_write_to_file = ""
        
        if i != 0 and i % 500 == 0:
            send_notif("Making progress on edges", f"Currently on i={i} out of {num_stops}", "success")

        for j in range(i + 1, num_stops):
            s1, s2 = all_stops[i], all_stops[j]

            if (s1 + s2) in already_calculated_edges:
                continue

            distance_in_min, shortest_path = -1, []
            try:
                distance_in_min = nx.shortest_path_length(nx_graph, s1, s2, weight="weight")
                shortest_path = nx.shortest_path(nx_graph, s1, s2, weight="weight")
            except:
                distance_in_min = floor(geodistance.distance(stops[s1], stops[s2]).km * KM_TO_TIME_MULTIPLE)
                shortest_path = [s1, s2]
            
            shortest_path_as_string = "-".join(shortest_path)
            edge_info = [s1, s2, str(distance_in_min), shortest_path_as_string]

            edges_to_write_to_file += ",".join(edge_info) + "\n"
            
        with open(edges_output_abs_file_path, "a") as output_stops_file:
            output_stops_file.write(edges_to_write_to_file)

    send_notif("All edges consolidated", f"Finished writing all edges between {s}-{e} to edge file.", "success")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("You need to provide 2 arguments, start and end int for i in the loop. For example, to get all edges starting from nodes 5-10:\n\t./edges.py 5 10")

    try:
        consolidate_edges()
    except Exception as e:
        send_notif("Edge consolidation crashed",f"Here is the error {e}.", "error")
        raise e