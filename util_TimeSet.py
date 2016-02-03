# EMF 		From...Import
from 	lib_TimeSet import DAYS, WEEKS, MONTHS, QUARTERS, YEARS, DT_EPOCH_ZERO, SECONDS
# System 	Import...As
import 	logging 			as 		log
import 	datetime
import 	pytz
import 	re
# System 	From...Import
from 	calendar 			import 	monthrange
from 	math 				import 	floor

def dt_is_end_of_month(datetime_):
	year_ = datetime_.year
	month_ = datetime_.month
	day_ = monthrange(year_, month_)[1]
	return (datetime_.day == day_ and 
			datetime_.hour == 0 and 
			datetime_.minute == 0 and 
			datetime_.second == 0)

def str_Y_M_D_is_end_of_month(str_):
	dt = dt_str_Y_M_D_to_datetime(str_)
	return dt_is_end_of_month(dt)

def dt_end_of_month(datetime_):
	year_ = datetime_.year
	month_ = datetime_.month
	day_ = monthrange(year_, month_)[1]
	return datetime.datetime(year_, month_, day_, tzinfo=pytz.UTC)

def dt_add_seconds(datetime_, seconds):
	epoch_ = dt_datetime_to_epoch(datetime_)
	epoch_ += seconds
	return dt_epoch_to_datetime(epoch_)

def dt_subtract_seconds(datetime_, seconds):
	epoch_ = dt_datetime_to_epoch(datetime_)
	epoch_ -= seconds
	return dt_epoch_to_datetime(epoch_)

def dt_subtract_months(datetime_, months):
	month_ = int((datetime_.month) - (months % 12))
	year_ = int(datetime_.year - floor(months/12.0) - int(month_<=0))
	month_ = int((month_) % 12 + 12*(month_%12==0)) #sloppy
	day_ = monthrange(year_, month_)[1]
	return datetime.datetime(year_, month_, day_, tzinfo=pytz.UTC)

def dt_add_months(datetime_, months):
	month_ = int((datetime_.month) + (months % 12))
	year_ = int(datetime_.year + floor(months/12.0) + int(month_>12))
	month_ = int((month_) % 12 + 12*(month_==12)) #sloppy
	day_ = monthrange(year_, month_)[1]
	return datetime.datetime(year_, month_, day_, tzinfo=pytz.UTC)

def dt_add_days(datetime_, days):
	return datetime_ + datetime.timedelta(days=days)

def dt_add_weeks(datetime_, weeks):
	return datetime_ + datetime.timedelta(weeks=weeks)

def dt_subtract_days(datetime_, days):
	return datetime_ + datetime.timedelta(days=-days)

def dt_subtract_weeks(datetime_, weeks):
	return datetime_ + datetime.timedelta(weeks=-weeks)

def dt_epoch_to_datetime(epoch_):
	return datetime.datetime.fromtimestamp(epoch_, pytz.UTC)

def dt_datetime_to_epoch(datetime_):
	return int((datetime_ - DT_EPOCH_ZERO).total_seconds())

def dt_now_as_epoch():
	dt = datetime.datetime.now(pytz.UTC)
	return int(dt_datetime_to_epoch(dt))

def dt_str_Y_M_D_to_datetime(dateString, endOfMonth=False):
	dt = datetime.datetime.strptime(dateString, '%Y-%m-%d')
	dt = dt.replace(tzinfo=pytz.UTC)
	if endOfMonth:
		dt = dt_end_of_month(dt)
	return dt

def dt_str_Y_M_D_Junk_to_epoch(dateString, endOfMonth=False):
	return dt_str_Y_M_D_to_epoch(dateString[:10], endOfMonth=endOfMonth)

def dt_str_Y_M_D_to_epoch(dateString, endOfMonth=False):
	dt = dt_str_Y_M_D_to_datetime(dateString, endOfMonth=endOfMonth)
	return dt_datetime_to_epoch(dt)

def dt_epoch_to_str_Y_M_D(epoch_):
	return strftime(dt_epoch_to_datetime(epoch_), '%Y-%m-%d', force=True)

def dt_epoch_to_str_Y_M_D_Time(epoch_):
	return strftime(dt_epoch_to_datetime(epoch_), '%Y-%m-%d %H:%M:%S', force=True)

def dt_epoch_to_str_YMD(epoch_):
	return strftime(dt_epoch_to_datetime(epoch_), '%Y%m%d', force=True)

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


# def main():
# 	print 'ADD'
# 	dt1 = dt_str_Y_M_D_to_datetime('2015-03-20',endOfMonth=True)
# 	dt2 = dt_add_months(dt1, 30)
# 	g = dt_date_range_generator(dt1, dt2, periodicity=QUARTERS, isEpoch=False)
# 	for i in g:
# 		print dt_epoch_to_datetime(i)
# 	print 'ADD'
# 	dt = dt_str_Y_M_D_to_datetime('2015-01-20',endOfMonth=True)
# 	for i in xrange(30):
# 		print dt_add_months(dt, i)
# 	print 'SUBTRACT'
# 	dt = dt_str_Y_M_D_to_datetime('2015-01-20',endOfMonth=True)
# 	for i in xrange(30):
# 		print dt_subtract_months(dt, i)


# if __name__ == '__main__':
# 	main()