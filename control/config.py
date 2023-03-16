# Should it output debug information in console
DEBUG_OUTPUT = True
DEBUG_MUST_INCLUDE = "looks like it is getting stuck"

# Time between syncs for busses and fleet management control call
BATCH_PERIOD_SEC = 30

# Number of buses in the fleet
FLEET_SIZE = 900

# For simulation time loop
NUM_SECONDS_IN_DAY = 86400

# Number of people that can fit on the bus
BUS_CAPACITY = 28

# max ok wait time before passenger is picked up
ACCEPTABLE_WAIT_FOR_PICKUP_SEC = 900 # 15 minutes

# max acceptable travel time from pickup as percent of direct path time
ACCEPTABLE_TRAVEL_DELAY_PERCENT = 1.5

# passenger requests must be >= this distance from start to dest
MIN_REQUEST_DISTANCE_KM = 3

# num simulated requests in the day
NUM_REQUESTS = 150_000

# center coordinates of high volume areas
HIGH_TRAFFIC_AREAS = [
    (45.394549, -75.662679),
    (45.395437, -75.712887),
    (45.269724, -75.74604),
    (45.365923, -75.731164),
    (45.434206, -75.666641),
]

# high traffic stops are this much more likely to be part of a trip than a regular stop
HIGH_TRAFFIC_STOPS_WEIGHT = 10

# all stops within 3km of any of the high traffic areas are classified as high traffic stops
HIGH_TRAFFIC_ZONE_RADIUS_KM = 3

# if geo distance is 10km, travel distance is = 10 * 1.4 = 14 min ~42.86km/hr avg aerial pace
KM_TO_MINUTES_MULTIPLE = 1.4
AVG_AERAL_PACE_KM_HR = (60 / KM_TO_MINUTES_MULTIPLE) # 42.86
AVG_AERAL_PACE_KM_SEC = AVG_AERAL_PACE_KM_HR / 3600 # 0.0119
AVG_AERAL_PACE_M_SEC = AVG_AERAL_PACE_KM_HR / 3.6 # 11.9