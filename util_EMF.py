# TODO: 
#	rename in underscore style

# EMF 		From...Import
from lib_EMF		 		import 	TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
# EMF 		Import...As
import lib_QuandlAPI
import lib_Logging
import lib_DB
# System 	Import...As
import 	logging 			as 		log
import 	datetime
# System 	From...Import
from 	calendar 			import 	monthrange


######################## DIRECTORY CODE
def get_EMF_settings(mode=TEMP_MODE):
	if mode==TEMP_MODE:
		return {
			'dbLoc':		lib_DB.TempDBFilePath,
			'overwriteDB':	True,
			'deleteDB':		True,
			'logLoc':		lib_Logging.TempLogFilePath,
			'recordLog':	False,
			'recordLevel':	log.DEBUG,
			'deleteLog':	True,
			'logAppend':	True,
			'QuandlCSVLoc': lib_QuandlAPI.TempQuandlCSV,
		}
	elif mode==TEST_MODE:
		return {
			'dbLoc':		lib_DB.TestDBFilePath,
			'overwriteDB':	True,
			'deleteDB':		False,
			'logLoc':		lib_Logging.TestLogFilePath,
			'recordLog':	False,
			'recordLevel':	log.DEBUG,
			'deleteLog':	False,
			'logAppend':	False,
			'QuandlCSVLoc': lib_QuandlAPI.TestQuandlCSV,
		}
	elif mode==QA_MODE:
		return {
			'dbLoc':		lib_DB.QADBFilePath,
			'overwriteDB':	False,
			'deleteDB':		False,
			'logLoc':		lib_Logging.QALogFilePath,
			'recordLog':	True,
			'recordLevel':	log.INFO,
			'deleteLog':	False,
			'logAppend':	True,
			'QuandlCSVLoc': lib_QuandlAPI.QAQuandlCSV,
		}
	elif mode==PROD_MODE:
		return {
			'dbLoc':		lib_DB.ProdDBFilePath,
			'overwriteDB':	False,
			'deleteDB':		False,
			'logLoc':		lib_Logging.ProdLogFilePath,
			'recordLog':	True,
			'recordLevel':	log.WARNING,
			'deleteLog':	False,
			'logAppend':	True,
			'QuandlCSVLoc': lib_QuandlAPI.ProdQuandlCSV,
		}
	else:
		raise NameError('EMF Run Mode not recognized')

######################## DATE TIME CODE
def dtGetDay(epochTime):
	return datetime.datetime.fromtimestamp(epochTime).day

def dtGetMonth(epochTime):
	return datetime.datetime.fromtimestamp(epochTime).month

def dtGetYear(epochTime):
	return datetime.datetime.fromtimestamp(epochTime).year

def dtGetNowAsEpoch():
	dt = datetime.datetime.now()
	return (dt-datetime.datetime(1970,1,1)).total_seconds()

def dtGetEndOfMonthAsEpoch(year, month):
	dt = datetime.datetime(year, month, monthrange(year, month)[1])
	return (dt-datetime.datetime(1970,1,1)).total_seconds()

def dtGetEndOfYearAsEpoch(year):
	dt = datetime.datetime(year, 12, 31)
	return (dt-datetime.datetime(1970,1,1)).total_seconds()

def dtConvert_YYYY_MM_DD_TimetoEpoch(timeString):
	dt = datetime.datetime.strptime(timeString, '%Y-%m-%d %H:%M:%S-%f')  
	return (dt-datetime.datetime(1970,1,1)).total_seconds()

def dtConvert_YYYY_MM_DDtoEpoch(timeString, endOfMonth=False):
	dt = datetime.datetime.strptime(timeString, '%Y-%m-%d')
	if endOfMonth:
		dt = dt.replace(day = monthrange(dt.year,dt.month)[1])
	return (dt-datetime.datetime(1970,1,1)).total_seconds()

def dtConvert_Mmm_YtoEpoch(timeString, endOfMonth=True):
	dt = datetime.datetime.strptime(timeString, '%b-%y')
	if endOfMonth:
		dt = dt.replace(day = monthrange(dt.year,dt.month)[1])
	return (dt-datetime.datetime(1970,1,1)).total_seconds()

def dtConvert_EpochtoY_M_D(epochTime):
	return strftime(datetime.datetime.fromtimestamp(epochTime), '%Y-%m-%d', force=True)

def dtConvert_EpochtoYMD(epochTime):
	return strftime(datetime.datetime.fromtimestamp(epochTime), '%Y%m%d', force=True)

# Taken from StackOverflow
def strftime(datetime_, format, force=False):
	"""`strftime()` that works for year < 1900.

	Disregard calendars shifts.

	>>> def f(fmt, force=False):
	...     return strftime(datetime(1895, 10, 6, 11, 1, 2), fmt, force)
	>>> f('abc %Y %m %D') 
	'abc 1895 10 10/06/95'
	>>> f('%X')
	'11:01:02'
	>>> f('%c') #doctest:+NORMALIZE_WHITESPACE
	Traceback (most recent call last):
	ValueError: '%c', '%x' produce unreliable results for year < 1900
	use force=True to override
	>>> f('%c', force=True)
	'Sun Oct  6 11:01:02 1895'
	>>> f('%x') #doctest:+NORMALIZE_WHITESPACE
	Traceback (most recent call last):
	ValueError: '%c', '%x' produce unreliable results for year < 1900
	use force=True to override
	>>> f('%x', force=True)
	'10/06/95'
	>>> f('%%x %%Y %Y')
	'%x %Y 1895'
	"""
	year = datetime_.year
	if year >= 1900:
	   return datetime_.strftime(format)

	# mMke year larger then 1900 using 400 increment
	# (Dates repeat every 400 years)
	assert year < 1900
	factor = (1900 - year - 1) // 400 + 1
	future_year = year + factor * 400
	assert future_year > 1900

	format = Specifier('%Y').replace_in(format, year)
	result = datetime_.replace(year=future_year).strftime(format)
	if any(f.ispresent_in(format) for f in map(Specifier, ['%c', '%x'])):
		msg = "'%c', '%x' produce unreliable results for year < 1900"
		if not force:
			raise ValueError(msg + " use force=True to override")
		warnings.warn(msg)
		result = result.replace(str(future_year), str(year))
	assert (future_year % 100) == (year % 100) # last two digits are the same
	return result

# Taken from StackOverflow
class Specifier(str):
	"""Model %Y and such in `strftime`'s format string."""
	def __new__(cls, *args):
		self = super(Specifier, cls).__new__(cls, *args)
		assert self.startswith('%')
		assert len(self) == 2
		self._regex = re.compile(r'(%*{0})'.format(str(self)))
		return self

	def ispresent_in(self, format):
		m = self._regex.search(format)
		return m and m.group(1).count('%') & 1 # odd number of '%'

	def replace_in(self, format, by):
		def repl(m):
			n = m.group(1).count('%')
			if n & 1: # odd number of '%'
				prefix = '%'*(n-1) if n > 0 else ''
				return prefix + str(by) # replace format
			else:
				return m.group(0) # leave unchanged
		return self._regex.sub(repl, format)
