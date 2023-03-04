# Should it output debug information in console
DEBUG_OUTPUT = False
DEBUG_MUST_INCLUDE = ""

# Time between syncs for busses and fleet management control call
BATCH_PERIOD_SEC = 30

# Number of buses in the fleet
FLEET_SIZE = 900

# For simulation time loop
NUM_SECONDS_IN_DAY = 86400

# Number of people that can fit on the bus
BUS_CAPACITY = 8

# max ok wait time before passenger is picked up
ACCEPTABLE_WAIT_FOR_PICKUP_SEC = 600 # 10 minutes

# max acceptable travel time from pickup as percent of direct path time
ACCEPTABLE_TRAVEL_DELAY_PERCENT = 1.3

# passenger requests must be >= this distance from start to dest
MIN_REQUEST_DISTANCE_KM = 3

# num simulated requests in the day
NUM_REQUESTS = 300_000

# stop ids of high volume stops
HIGH_TRAFFIC_STOPS = ["7175","6790","7367","1249","2997","8783"]

# high traffic stops are this much more likely to be part of a trip than a regular stop
HIGH_TRAFFIC_STOPS_WEIGHT = 10

# if geo distance is 10km, travel distance is = 10 * 1.4 = 14 min ~42.86km/hr avg aerial pace
KM_TO_MINUTES_MULTIPLE = 1.4
AVG_AERAL_PACE_KM_HR = (60 / KM_TO_MINUTES_MULTIPLE) # 42.86
AVG_AERAL_PACE_KM_SEC = AVG_AERAL_PACE_KM_HR / 3600 # 0.0119
AVG_AERAL_PACE_M_SEC = AVG_AERAL_PACE_KM_HR / 3.6 # 11.9