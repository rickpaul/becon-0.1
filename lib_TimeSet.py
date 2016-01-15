import datetime
import pytz

DT_EPOCH_ZERO = datetime.datetime.fromtimestamp(0, pytz.UTC) # datetime.datetime(1970,1,1,0)

DAYS = 24*60*60
WEEKS = 7*DAYS
MONTHS = 4*WEEKS
QUARTERS = 3*MONTHS
YEARS = 4*QUARTERS

DATESTRING_TYPE = 389172
DATETIME_TYPE = 892461
EPOCH_TYPE = 476512