from datetime import datetime
import pytz
from dateutil.rrule import rrule, MINUTELY
import datetime
import bisect


def convert_epoch(epoch):
    dt = datetime.datetime.utcfromtimestamp(epoch)
    dt = dt.replace(tzinfo=pytz.UTC)
    return dt


def get_closest_thirty(dt, direction, resolution=30):
    new_minute = (dt.minute // resolution + (1 if direction == 'up' else 0)) * resolution
    return dt + datetime.timedelta(minutes=new_minute - dt.minute)


def format_liveatc_time(dt):
    return dt.strftime("%b-%d-%Y-%H%MZ")