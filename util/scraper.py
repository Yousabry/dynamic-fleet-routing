from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os
import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("You need to provide 2 arguments, start and end node for a. For example, to get all paths starting from nodes 5-10:\n\t./scraper.py 5 10")

    script_dir = os.path.dirname(__file__)
    target_abs_file_path = os.path.join(script_dir, "../data/clean_stops.txt")
    
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    def get_distance(driver, url):
        timeToDriveComponentXpath = "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]"
        timeToWalkComponentXpath =  "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div/div[1]/div[3]/div[1]/div[1]"
        timeToWalk2ComponentXpath = "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[2]/div[1]/div[3]/div[1]/div[1]"

        xpath_attempts = [timeToDriveComponentXpath, timeToWalkComponentXpath, timeToWalk2ComponentXpath]

        try:
            driver.get(url)

            for i, xpath in enumerate(xpath_attempts):
                try:
                    travel_time = driver.find_element(By.XPATH, xpath).text

                    if "min" in travel_time:
                        if i > 0:
                            travel_time += " walk"
                        return travel_time

                except:
                    pass
        except:
            pass

        return "-1"

    def write_to_edges_file(a: int, textToWrite: str):
        # we will have 50 edge weight files
        x = a % 50
        edges_abs_file_path = os.path.join(script_dir, f"../data/edge_weights{x}.txt")

        with open(edges_abs_file_path, "a") as edges_file:
            edges_file.write(textToWrite)

    def write_to_failures_file(url: str):
        failures_abs_file_path = os.path.join(script_dir, f"../data/failures.txt")

        with open(failures_abs_file_path, "a") as fail_file:
            fail_file.write(f"{url}\n")

    def get_already_calculated_edges(a: int):
        # we have 50 edge weight files
        x = a % 50
        edges_abs_file_path = os.path.join(script_dir, f"../data/edge_weights{x}.txt")
        already_calculated = {}

        if not os.path.isfile(edges_abs_file_path):
            return already_calculated

        with open(edges_abs_file_path, "r") as edges_file:
            for edge_info in edges_file:
                try:
                    [stop1, stop2, time] = edge_info.strip().split(",")
                    already_calculated[str(stop1+stop2)] = time
                except:
                    continue

        return already_calculated

    def send_notif(message, description, type):
        requests.post("https://api.mynotifier.app", {
            "apiKey": 'd3afbf45-1111-4e4e-9d9a-5ec95ac88698',
            "message": message,
            "description": description,
            "project": "f97186",
            "type": type, # info, error, warning or success
        })

    def get_all_stops_info():
        # read all stops info
        stops = []
        with open(target_abs_file_path, "r") as file:
            stops = [line.strip().split(',') for line in file]

        return stops

    def scrape_edges_for_a_vals(start: int, endExclusive: int):
        stops = get_all_stops_info()
        n = len(stops)
        failures, successes, skipped = 0, 0, 0

        for a in range(start, endExclusive):
            already_done = get_already_calculated_edges(a)
            [street, crossStreet, stopId] = stops[a]

            for b in range(a+1, n):
                [street2, crossStreet2, stopId2] = stops[b]

                if str(stopId+stopId2) in already_done:
                    skipped += 1
                    continue

                origin = f"{street}+{crossStreet},+Ottawa,+ON"
                dest = f"{street2}+{crossStreet2},+Ottawa,+ON"
                url = f'https://www.google.com/maps/dir/{origin}/{dest}/'

                d = get_distance(driver, url)

                if d == "-1":
                    failures += 1
                    if failures < 1000:
                        write_to_failures_file(url)
                else:
                    successes += 1
                    write_to_edges_file(a, f'{stopId},{stopId2},{d}\n')

        send_notif("Finished job!",f"Finished edges from {start} to {endExclusive} exclusive. {successes} successes, {failures} failures, {skipped} skipped.","success")

    try:
        s, e = int(sys.argv[1]), int(sys.argv[2]) + 1
        scrape_edges_for_a_vals(s, e)
    except Exception as e:
        driver.quit()
        send_notif("Threw an error!", f"Trying to scrape edges {sys.argv[1]} to {int(sys.argv[2]) + 1}. {str(e)}", "error")
