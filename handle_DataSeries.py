# TODOS:
#	create way to select random data series
#	create way to select random data series according to criteria
#		e.g. min_date, max_date, periodicity, 
#	save maxDateEncountered, minDateEncountered, etc.
#	we insert but we don't retrieve isInterpolated, isForecast
#	Find a way to make sure that data history date/times match up (create canonical dates fn)
#	Do we really want to allow dataSeries unsetting? Should make you delete object
#	Refactor [e.g. unset_data_series --> unset]
#		Implement template class for Handles?

# EMF 		From...Import
from	util_EMF		import 	dtGetNowAsEpoch, dtGetMonth, dtGetYear
from 	lib_DataSeries	import 	DATE_COL, VALUE_COL, DATA_HISTORY_DTYPE
# System 	Import...As
import 	lib_DBInstructions 	as 	lib_DBInst
import 	logging 			as 	log
import 	numpy 				as 	np
# System 	From...Import
from 	sys 			import 	maxint


class EMF_DataSeries_Handle:
	def __init__(self, dbHandle):
		self.hndl_DB = dbHandle
		self.seriesID = None
		self.dataHistory = None

	def __str__(self):
		assert self.seriesID is not None
		return self.seriesTicker

	def __get_from_DB(self, column):
		return lib_DBInst.retrieve_DataSeriesMetaData(self.hndl_DB.cursor_(), column, self.seriesID)

	def __send_to_DB(self, column, value):
		return lib_DBInst.update_DataSeriesMetaData(self.hndl_DB.conn_(), self.hndl_DB.cursor_(), column, value, self.seriesID)

	def is_set(self):
		return self.seriesID is not None

	def set_data_series(self, name=None, ticker=None, insertIfNot=True):
		assert self.seriesID is None # Force reset before setting (Or new object)
		self.seriesID = lib_DBInst.retrieve_DataSeriesID(	self.hndl_DB.conn_(), 
															self.hndl_DB.cursor_(),
															name=name,
															ticker=ticker,
															insertIfNot=insertIfNot)
		assert self.seriesID is not None # Did we catch something?
		if name is None: name = self.__get_from_DB('txt_data_name')
		self.seriesName = name
		if ticker is None: ticker = self.__get_from_DB('txt_data_ticker')
		self.seriesTicker = ticker
		return self.seriesID

	def unset_data_series(self):
		self.dataHistory = None
		self.seriesID = None
		self.seriesName = None
		self.seriesTicker = None

	def get_data_history(self, saveHistoryLocal=False):
		'''
		TODOS:
					We have no way to retrieve whether is interpolated or is forecast
		'''
		assert self.seriesID is not None
		dataSeries = lib_DBInst.getCompleteDataHistory_DataHistoryTable(self.hndl_DB.cursor_(), self.seriesID)
		dataSeries = np.asarray(dataSeries, dtype=DATA_HISTORY_DTYPE)
		if saveHistoryLocal:
			self.dataHistory = dataSeries
		return dataSeries

	def __insert_data_point(self, date, value, isInterpolated=False, isForecast=False):
		'''
		CONSIDER:
		Is it appropriate to cast values here? I think so....
		'''
		return lib_DBInst.insertDataPoint_DataHistoryTable( self.hndl_DB.conn_(), self.hndl_DB.cursor_(), 
															self.seriesID, 
															int(date), 
															float(value), 
															interpolated=int(isInterpolated),
															forecast=int(isForecast))

	def insert_data_history(self, dates, values, isInterpolated=None, isForecast=None, saveHistoryLocal=True):
		'''
		TODOS: 
					Figure out what format dates, values, should come in [numpy array vs int] (to avoid weird casting errors)
					Store Data on successful inserts, maxDateEncountered, etc.
							What are we doing with dates we find?
		'''
		assert self.seriesID is not None
		dataLen = len(dates)
		assert dates.shape == values.shape
		hasInt = (isInterpolated is not None)
		hasFor = (isForecast is not None)
		if hasInt:
			assert dates.shape == isInterpolated.shape
		if hasFor:
			assert dates.shape == isForecast.shape
		successfulInserts = 0
		unsuccessfulInserts = 0
		minDate = maxint
		maxDate = -maxint-1
		for i in range(dataLen):
			isInt = hasInt and isInterpolated[i]
			isFor = hasFor and isForecast[i]
			date = dates[i]
			success = self.__insert_data_point(date, values[i], isInt, isFor)
			if not success:
				log.warning('Failed to Write Historical Data Point at %s for %s [value = %f]', self.seriesTicker, dates[i], values[i])
				unsuccessfulInserts += 1
			else:
				minDate = min(date, minDate) 
				maxDate = max(date, maxDate)
				successfulInserts +=1
		log.info('Successfully/Unsuccessfully wrote %d/%d Historical Data Points for %s', successfulInserts, unsuccessfulInserts, self.seriesTicker)
		self.__send_to_DB('dt_last_updated_history', dtGetNowAsEpoch())
		if saveHistoryLocal:
			self.dataHistory = np.asarray(np.hstack((dates, values)), dtype=DATA_HISTORY_DTYPE)
		return (successfulInserts, unsuccessfulInserts)

	# def get_latest_date(self):
	# 	raise NotImplementedError

	# def check_data_fullness(self, earliestDate, latestDate, periodicity=12):
	# 	'''
	# 	This method checks if the data is filled in (i.e. if data is monthly since 1990, 
	# 		every year should have) 12 points at expected times.
	# 	'''
	# 	raise NotImplementedError # How to deal with non-months?
	# 	assert periodicity == 12 or periodicity == 1 or periodicity == 4 or periodicity == 52 or periodicity == 365

	# 	startDay = dtGetDay(earliestDate)
	# 	startMonth = dtGetMonth(earliestDate)
	# 	startYear = dtGetYear(earliestDate)
	# 	endDay = dtGetDay(earliestDate)
	# 	endMonth = dtGetMonth(earliestDate)
	# 	endYear = dtGetYear(earliestDate)
	# 	lib_DBInst.getCompleteDataHistory_DataHistoryTable(self.hndl_DB.cursor_(), self.seriesID)


