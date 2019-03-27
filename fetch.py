import pytz, datetime
import configparser
from apis import flightaware
import utils
from apis import liveatc
import time
config = configparser.ConfigParser()
config.read('config.conf')

local = pytz.timezone ("US/Eastern")
naive = datetime.datetime.strptime ("2019-03-26 15:45:00", "%Y-%m-%d %H:%M:%S")
local_dt = local.localize(naive)
utc_dt = local_dt.astimezone(pytz.utc)

# print(local_dt)
# print(utc_dt)

timestamp = int(utc_dt.timestamp())

client = flightaware.FlightAware(config['API-KEYS']['flightaware_username'], config['API-KEYS']['flightaware_key'])



flights = client.flight_search("SWA8701")

print(client.get_last_track("DAL1"))
exit()
client.pretty_print_flight_info_short(flights[0])
origin = flights[0]['origin']
depart_time = client.get_latest_flight_takeoff_time("SWA8701")
depart_time = utils.convert_epoch(depart_time)
print("Actual takeoff time: %s-ish" % utils.format_liveatc_time(depart_time))

rounded_depart_time = utils.get_closest_thirty(depart_time, "down")
liveatc_formated = utils.format_liveatc_time(rounded_depart_time)

liveatc_feeds = liveatc.get_airport(origin)
for each in liveatc_feeds:
    print("Getting archives from %s (%s)" % (each, liveatc_formated))
    liveatc.get_audio(origin, each, liveatc_formated)
    print("Sleeping for 10s")
    time.sleep(10)

#client.get_flight_id("SWA8701", 1553626065)
#client.get_last_track("SWA8701")
#client.get_historical_flight_map("SWA8701-1553613485-0-0-78")