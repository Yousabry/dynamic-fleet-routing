# This util cleans up all stops data needed into one stops.txt
import os 

DATA_PATH = '../data/'

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    clean_stops_abs_file_path = os.path.join(script_dir, f"{DATA_PATH}/clean_stops.txt")
    oc_stops_abs_file_path = os.path.join(script_dir, f"{DATA_PATH}/oc_stops.txt")
    output_stops_file_path = os.path.join(script_dir, f"{DATA_PATH}/stops.txt")


    clean_stops = {}

    with open(clean_stops_abs_file_path, "r") as clean_stops_file:
        for stop in clean_stops_file:
            [street, crossStreet, stop_code] = stop.strip().split(",")
            clean_stops[stop_code] = False
    
    with open(output_stops_file_path, "w") as output_stops_file:
        output_stops_file.write("stop_id,stop_code,stop_name,stop_lat,stop_lon\n")

        with open(oc_stops_abs_file_path, "r") as oc_transpo_file:
            for stop in oc_transpo_file:
                [stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type] = stop.strip().split(",")
                
                if stop_code not in clean_stops:
                    continue

                clean_stops[stop_code] = True
                s = [stop_id,stop_code,stop_name,stop_lat,stop_lon]
                output_stops_file.write(",".join(s) + "\n")
