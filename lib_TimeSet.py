# System 	Import...As
import datetime
import pytz

DT_EPOCH_ZERO = datetime.datetime.fromtimestamp(0, pytz.UTC) # datetime.datetime(1970,1,1,0)

SECONDS 	= 1
DAYS 		= 24*60*60
WEEKS 		= 7*DAYS
MONTHS 		= 4*WEEKS
QUARTERS 	= 3*MONTHS
YEARS 		= 4*QUARTERS

DATESTRING_TYPE = 'DS'
DATETIME_TYPE 	= 'DT'
EPOCH_TYPE 		= 'E'