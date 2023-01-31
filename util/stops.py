# This util cleans up all stops data needed into one stops.txt
import os 

DATA_PATH = '../data/'

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    stops_file_path = os.path.join(script_dir, f"{DATA_PATH}/stops.txt")
    output_stops_file_path = os.path.join(script_dir, f"{DATA_PATH}/stops2.txt")


    clean_stops = {}

    with open(stops_file_path, "r") as stops_file:
        with open(output_stops_file_path, "w") as output_stops_file:
            output_stops_file.write("stop_id,stop_code,stop_name,stop_lat,stop_lon\n")


            for stop in stops_file:
                [stop_id,stop_code,stop_name,stop_lat,stop_lon] = stop.strip().split(",")
                stop_lat = stop_lat.strip()
                stop_lon = stop_lon.strip()

                s = [stop_id,stop_code,stop_name,stop_lat,stop_lon]
                output_stops_file.write(",".join(s) + "\n")
                