import datetime
import pytz

DT_EPOCH_ZERO = datetime.datetime.fromtimestamp(0, pytz.UTC) # datetime.datetime(1970,1,1,0)

SECONDS = 1
DAYS = 24*60*60
WEEKS = 7*DAYS
MONTHS = 4*WEEKS
QUARTERS = 3*MONTHS
YEARS = 4*QUARTERS

DATESTRING_TYPE = 389172 # Random
DATETIME_TYPE = 892461 # Random
EPOCH_TYPE = 476512 # Random