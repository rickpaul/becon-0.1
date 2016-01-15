# EMF 		From...Import
from 	lib_TimeSet 	import DAYS, WEEKS, MONTHS, QUARTERS, YEARS
from 	lib_TimeSet 	import DATESTRING_TYPE, DATETIME_TYPE, EPOCH_TYPE
from 	util_TimeSet 	import dt_epoch_to_datetime, dt_datetime_to_epoch
from 	util_TimeSet 	import dt_add_months, dt_subtract_months, strftime
from 	util_TimeSet 	import dt_str_Y_M_D_to_datetime
# System 	Import...As
import 	datetime


class EMF_DateTime_Handle(object):
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
		if self.periodicity == MONTHS:
			self.startDT = dt_add_months(self.startDT, 1*numPeriods)
			self.endDT = dt_add_months(self.endDT, 1*numPeriods)
		elif self.periodicity == QUARTERS:
			self.startDT = dt_add_months(self.startDT, 3*numPeriods)
			self.endDT = dt_add_months(self.endDT, 3*numPeriods)
		elif self.periodicity == YEARS:
			self.startDT = dt_add_months(self.startDT, 12*numPeriods)
			self.endDT = dt_add_months(self.endDT, 12*numPeriods)
		else:
			raise NotImplementedError

	def shift_backwards(self, numPeriods):
		if self.periodicity == MONTHS:
			self.startDT = dt_subtract_months(self.startDT, 1*numPeriods)
			self.endDT = dt_subtract_months(self.endDT, 1*numPeriods)
		elif self.periodicity == QUARTERS:
			self.startDT = dt_subtract_months(self.startDT, 3*numPeriods)
			self.endDT = dt_subtract_months(self.endDT, 3*numPeriods)
		elif self.periodicity == YEARS:
			self.startDT = dt_subtract_months(self.startDT, 12*numPeriods)
			self.endDT = dt_subtract_months(self.endDT, 12*numPeriods)
		else:
			raise NotImplementedError

	def truncate_end(self, numPeriods):
		if self.periodicity == MONTHS:
			self.endDT = dt_subtract_months(self.endDT, 1*numPeriods)
		elif self.periodicity == QUARTERS:
			self.endDT = dt_subtract_months(self.endDT, 3*numPeriods)
		elif self.periodicity == YEARS:
			self.endDT = dt_subtract_months(self.endDT, 12*numPeriods)
		else:
			raise NotImplementedError

	def truncate_start(self, numPeriods):
		if self.periodicity == MONTHS:
			self.startDT = dt_add_months(self.startDT, 1*numPeriods)
		elif self.periodicity == QUARTERS:
			self.startDT = dt_add_months(self.startDT, 3*numPeriods)
		elif self.periodicity == YEARS:
			self.startDT = dt_add_months(self.startDT, 12*numPeriods)
		else:
			raise NotImplementedError

	def get_date_range_generator(self, outputType=EPOCH_TYPE):
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
			if self.periodicity == MONTHS:
				currentDT = dt_add_months(currentDT, 1)
			elif self.periodicity == QUARTERS:
				currentDT = dt_add_months(currentDT, 3)
			elif self.periodicity == YEARS:
				currentDT = dt_add_months(currentDT, 12)
			else:
				raise NotImplementedError
		# Yield End
		yield outputFn(self.endDT)

	def get_date_range(self, outputType=EPOCH_TYPE):
		generator = self.get_date_range_generator(outputType=outputType)
		return [d for d in generator]


if __name__ == '__main__':
	x = EMF_DateTime_Handle()
	x.startYMD = '1980-01-01'
	x.endYMD = '1981-01-01'
	x.periodicity = MONTHS
	x.truncate_end(2)
	print x.startDT
	print x.endDT
	print x.get_date_range(outputType=DATESTRING_TYPE)