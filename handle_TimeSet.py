# TODO:
# 	Change so only holds datetime, makes conversions on request (lighter object)

# EMF 		From...Import
from 	lib_TimeSet 	import DAYS, WEEKS, MONTHS, QUARTERS, YEARS, SECONDS
from 	lib_TimeSet 	import DATESTRING_TYPE, DATETIME_TYPE, EPOCH_TYPE
from 	util_TimeSet 	import dt_epoch_to_datetime, dt_datetime_to_epoch
from 	util_TimeSet 	import dt_add_months, dt_subtract_months, strftime
from 	util_TimeSet 	import dt_add_seconds, dt_subtract_seconds
from 	util_TimeSet 	import dt_str_Y_M_D_to_datetime
# System 	Import...As
import 	datetime
import 	numpy 			as np

def min_time_handle_merge(hndl_Time1, hndl_Time2):
	hndl_Time = EMF_TimeSet_Handle()
	hndl_Time.startEpoch = max(hndl_Time1.startEpoch, hndl_Time2.startEpoch)
	hndl_Time.endEpoch = min(hndl_Time1.endEpoch, hndl_Time2.endEpoch)
	hndl_Time.periodicity = max(hndl_Time1.periodicity, hndl_Time2.periodicity)
	return hndl_Time

def max_time_handle_merge(hndl_Time1, hndl_Time2):
	hndl_Time = EMF_TimeSet_Handle()
	hndl_Time.startEpoch = min(hndl_Time1.startEpoch, hndl_Time2.startEpoch)
	hndl_Time.endEpoch = max(hndl_Time1.endEpoch, hndl_Time2.endEpoch)
	hndl_Time.periodicity = min(hndl_Time1.periodicity, hndl_Time2.periodicity)
	return hndl_Time

def verify_date_series(date_series, type_=EPOCH_TYPE, periodicity_=MONTHS):
	hndl_Time = EMF_TimeSet_Handle()
	hndl_Time.periodicity = periodicity_
	if type_ == EPOCH_TYPE:
		hndl_Time.startEpoch = date_series[0]
		hndl_Time.endEpoch = date_series[-1]
	elif type_ == DATETIME_TYPE:
		hndl_Time.startDT = date_series[0]
		hndl_Time.endDT = date_series[-1]
	elif type_ == DATESTRING_TYPE:
		hndl_Time.startYMD = date_series[0]
		hndl_Time.endYMD = date_series[-1]
	else:
		raise NameError
	generator = hndl_Time.get_date_generator(type=type_)
	for (gen_dt, ser_dt) in zip(generator, date_series):
		if gen_dt != ser_dt:
			return False
	return True

class EMF_TimeSet_Handle(object):
	def __init__(self):
		_startYMD = None
		_endYMD = None
		_startEpoch = None
		_startDT = None
		_endEpoch = None
		_endDT = None
		_periodicity = None

	def startYMD():
		doc = "Start Y-M-D"
		def fget(self):
			return self._startYMD
		def fset(self, value):
			if type(value) is not str:
				raise TypeError
			self._startYMD  = value
			self._startDT = dt_str_Y_M_D_to_datetime(value)
			self._startEpoch = dt_datetime_to_epoch(self._startDT)
		def fdel(self):
			del self._startYMD
		return locals()
	startYMD = property(**startYMD())

	def endYMD():
		doc = "End Y-M-D"
		def fget(self):
			return self._endYMD
		def fset(self, value):
			if type(value) is not str:
				raise TypeError
			self._endYMD  = value
			self._endDT = dt_str_Y_M_D_to_datetime(value)
			self._endEpoch = dt_datetime_to_epoch(self._endDT)
		def fdel(self):
			del self._endYMD
		return locals()
	endYMD = property(**endYMD())

	def startEpoch():
		doc = "Start Epoch"
		def fget(self):
			return self._startEpoch
		def fset(self, value):
			if type(value) is not int:
				raise TypeError
			self._startEpoch = value
			self._startDT = dt_epoch_to_datetime(value)
			self._startYMD = strftime(self._startDT, '%Y-%m-%d')
		def fdel(self):
			del self._startEpoch
		return locals()
	startEpoch = property(**startEpoch())

	def endEpoch():
		doc = "End Epoch"
		def fget(self):
			return self._endEpoch
		def fset(self, value):
			if type(value) is not int:
				raise TypeError
			self._endEpoch = value
			self._endDT = dt_epoch_to_datetime(value)
			self._endYMD = strftime(self._endDT, '%Y-%m-%d')
		def fdel(self):
			del self._endEpoch
		return locals()
	endEpoch = property(**endEpoch())

	def startDT():
		doc = "Start Datetime"
		def fget(self):
			return self._startDT
		def fset(self, value):
			if type(value) is not datetime.datetime:
				raise TypeError
			self._startDT = value
			self._startEpoch = dt_datetime_to_epoch(value)
			self._startYMD = strftime(self._startDT, '%Y-%m-%d')
		def fdel(self):
			del self._startDT
		return locals()
	startDT = property(**startDT())

	def endDT():
		doc = "End Datetime"
		def fget(self):
			return self._endDT
		def fset(self, value):
			if type(value) is not datetime.datetime:
				raise TypeError
			self._endDT = value
			self._endEpoch = dt_datetime_to_epoch(value)
			self._endYMD = strftime(self._endDT, '%Y-%m-%d')
		def fdel(self):
			del self._endDT
		return locals()
	endDT = property(**endDT())

	def periodicity():
		doc = "Periodicity"
		def fget(self):
			return self._periodicity
		def fset(self, value):
			if type(value) is not int:
				raise TypeError
			self._periodicity = value
		def fdel(self):
			del self._periodicity
		return locals()
	periodicity = property(**periodicity())

	def shift_forward(self, numPeriods):
		if self.periodicity == SECONDS:
			self.startDT = dt_add_seconds(self.startDT, numPeriods)
			self.endDT = dt_add_seconds(self.endDT, numPeriods)
		elif self.periodicity == MONTHS:
			self.startDT = dt_add_months(self.startDT, numPeriods)
			self.endDT = dt_add_months(self.endDT, numPeriods)
		elif self.periodicity == QUARTERS:
			self.startDT = dt_add_months(self.startDT, 3*numPeriods)
			self.endDT = dt_add_months(self.endDT, 3*numPeriods)
		elif self.periodicity == YEARS:
			self.startDT = dt_add_months(self.startDT, 12*numPeriods)
			self.endDT = dt_add_months(self.endDT, 12*numPeriods)
		else:
			raise NotImplementedError

	def shift_backward(self, numPeriods):
		if self.periodicity == SECONDS:
			self.startDT = dt_subtract_seconds(self.startDT, numPeriods)
			self.endDT = dt_subtract_seconds(self.endDT, numPeriods)
		elif self.periodicity == MONTHS:
			self.startDT = dt_subtract_months(self.startDT, numPeriods)
			self.endDT = dt_subtract_months(self.endDT, numPeriods)
		elif self.periodicity == QUARTERS:
			self.startDT = dt_subtract_months(self.startDT, 3*numPeriods)
			self.endDT = dt_subtract_months(self.endDT, 3*numPeriods)
		elif self.periodicity == YEARS:
			self.startDT = dt_subtract_months(self.startDT, 12*numPeriods)
			self.endDT = dt_subtract_months(self.endDT, 12*numPeriods)
		else:
			raise NotImplementedError

	def truncate_end(self, numPeriods):
		if self.periodicity == SECONDS:
			self.endDT = dt_subtract_seconds(self.endDT, numPeriods)
		elif self.periodicity == MONTHS:
			self.endDT = dt_subtract_months(self.endDT, numPeriods)
		elif self.periodicity == QUARTERS:
			self.endDT = dt_subtract_months(self.endDT, 3*numPeriods)
		elif self.periodicity == YEARS:
			self.endDT = dt_subtract_months(self.endDT, 12*numPeriods)
		else:
			raise NotImplementedError

	def truncate_start(self, numPeriods):
		if self.periodicity == SECONDS:
			self.startDT = dt_add_seconds(self.startDT, numPeriods)
		elif self.periodicity == MONTHS:
			self.startDT = dt_add_months(self.startDT, numPeriods)
		elif self.periodicity == QUARTERS:
			self.startDT = dt_add_months(self.startDT, 3*numPeriods)
		elif self.periodicity == YEARS:
			self.startDT = dt_add_months(self.startDT, 12*numPeriods)
		else:
			raise NotImplementedError

	def get_date_generator(self, outputType=EPOCH_TYPE):
		# Set Output Function
		if outputType==DATETIME_TYPE:
			outputFn = lambda d: d
		elif outputType==EPOCH_TYPE:
			outputFn = dt_datetime_to_epoch
		elif outputType==DATESTRING_TYPE:
			outputFn = lambda d: strftime(d, '%Y-%m-%d')
		else:
			raise NameError
		# Yield Dates
		currentDT = self.startDT
		while currentDT < self.endDT:
			yield outputFn(currentDT)
			if self.periodicity == SECONDS:
				currentDT = dt_add_seconds(currentDT, 1)
			elif self.periodicity == MONTHS:
				currentDT = dt_add_months(currentDT, 1)
			elif self.periodicity == QUARTERS:
				currentDT = dt_add_months(currentDT, 3)
			elif self.periodicity == YEARS:
				currentDT = dt_add_months(currentDT, 12)
			else:
				raise NotImplementedError
		# Yield End
		yield outputFn(self.endDT)

	def get_dates(self, outputType=EPOCH_TYPE):
		generator = self.get_date_generator(outputType=outputType)
		return np.array([d for d in generator])

	def get_date_filter(self, min_, max_, inputType=EPOCH_TYPE):
		for date in self.get_date_generator(outputType=inputType):
			if date >= min_ and date <= max_:
				yield True
			else:
				yield False

	# def start_date_earlier(self, numPeriods): # do we want this?
	# 	if self.periodicity == MONTHS:
	# 		return dt_subtract_months(self.startDT, 1*numPeriods)
	# 	elif self.periodicity == QUARTERS:
	# 		return dt_subtract_months(self.startDT, 3*numPeriods)
	# 	elif self.periodicity == YEARS:
	# 		return dt_subtract_months(self.startDT, 12*numPeriods)
	# 	else:
	# 		raise NotImplementedError

	# def end_date_later(self, numPeriods): # do we want this?
	# 	if self.periodicity == MONTHS:
	# 		return dt_add_months(self.startDT, 1*numPeriods)
	# 	elif self.periodicity == QUARTERS:
	# 		return dt_add_months(self.startDT, 3*numPeriods)
	# 	elif self.periodicity == YEARS:
	# 		return dt_add_months(self.startDT, 12*numPeriods)
	# 	else:
	# 		raise NotImplementedError

if __name__ == '__main__':
	x = EMF_TimeSet_Handle()
	x.startYMD = '1980-01-01'
	x.endYMD = '1982-01-01'
	x.periodicity = MONTHS
	x.truncate_end(2)
	print x.startDT
	print x.endDT
	print x.get_dates(outputType=DATESTRING_TYPE)
	print [y for y in x.get_date_filter('1980-06-01', '1981-06-01', DATESTRING_TYPE)]