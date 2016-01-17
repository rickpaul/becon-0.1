# TODOS:
#	we insert but we don't retrieve isInterpolated, isForecast
#	Make periodicity a required field for insertion?
# 	use verify_date_series
# 	Make all get_set into properties
# 		transform __get from db into __load_metadata
# 		transform __save to db into __save_metadata

# EMF 		From...Import
from 	handle_TimeSet 			import EMF_TimeSet_Handle, verify_date_series
from 	lib_DataSeries			import DATE_COL, VALUE_COL, DATA_HISTORY_DTYPE
from 	lib_JSON				import JSONRepository, DATA_SERIES_TO_JSON
from 	template_SerialHandle 	import EMF_Serial_Handle
from 	util_DB					import typify
from	util_TimeSet			import dt_now_as_epoch
# EMF 		Import...As
import 	lib_DBInstructions 		as lib_DBInst
# System 	Import...As
import 	logging 				as log
import 	numpy 					as np
# System 	From...Import
from 	sys 					import maxint
from 	json 					import dumps as json_dump

class EMF_DataSeries_Handle(EMF_Serial_Handle):
	def __init__(self, dbHandle, name=None, ticker=None, periodicity=None, insertIfNot=False):
		self._hndl_DB = dbHandle
		self._hndl_Time = None
		self.stored_series = None
		self._metadataCache = {}
		self.seriesID = lib_DBInst.retrieve_DataSeriesID(	self._hndl_DB.conn, 
															self._hndl_DB.cursor,
															name=name,
															ticker=ticker,
															periodicity=periodicity,
															insertIfNot=insertIfNot)
		assert self.seriesID is not None # Did we catch something?
		if name is None: name = self.__get_from_DB('txt_data_name')
		self.seriesName = name
		if ticker is None: ticker = self.__get_from_DB('txt_data_ticker')
		self.seriesTicker = ticker

	def __str__(self):
		return self.seriesTicker

	def __get_from_DB(self, column):
		if column in self._metadataCache:
			return self._metadataCache[column]
		value = lib_DBInst.retrieve_DataSeriesMetaData(self._hndl_DB.cursor, column, self.seriesID)
		self._metadataCache[column] = value
		return value

	def __send_to_DB(self, column, value):
		success = lib_DBInst.update_DataSeriesMetaData(self._hndl_DB.conn, self._hndl_DB.cursor, column, value, self.seriesID)
		if success:
			self._metadataCache[column] = value
		else:
			raise NotImplementedError #How 

	def __get_series(self, regenerate=False):
		# If Stored, Return
		if (self.stored_series is not None) and (not regenerate):
			return self.stored_series
		# If not Stored, Get Data from DB
		else:
			dataSeries = lib_DBInst.getCompleteDataHistory_DataHistoryTable(self._hndl_DB.cursor, self.seriesID)
			dataSeries = np.asarray(dataSeries, dtype=DATA_HISTORY_DTYPE)
			self.set_num_points(len(dataSeries))
			return dataSeries

	# def get_series_values_filtered(self, min_, max_):
	# 	series = self.__get_series()
	# 	filter_ = np.logical_and(series[DATE_COL]>=min_, series[DATE_COL]<=max_)
	# 	return np.reshape(series[filter_][VALUE_COL], (sum(filter_), 1))

	# def get_series_dates_filtered(self, min_, max_):
	# 	series = self.__get_series()
	# 	filter_ = np.logical_and(series[DATE_COL]>=min_, series[DATE_COL]<=max_)
	# 	return np.reshape(series[filter_][DATE_COL], (sum(filter_), 1))

	def get_series_values(self):
		'''
		TODOS:
					We have no way to retrieve whether is interpolated or is forecast
		'''
		return self.__get_series()[VALUE_COL]

	def get_series_dates(self):
		'''
		TODOS:
					Can we replace this with get_date_handle?

		'''
		return self.__get_series()[DATE_COL]

	def hndl_Time():
		doc = "Get Time Handle."
		def fget(self):
			if self._hndl_Time is None:
				self._hndl_Time = EMF_TimeSet_Handle()
				self._hndl_Time.periodicity = self.get_periodicity()
				self._hndl_Time.startEpoch = self.get_earliest_date()
				self._hndl_Time.endEpoch = self.get_latest_date()
			return self._hndl_Time
		def fdel(self):
			del self._hndl_Time
		return locals()
	hndl_Time = property(**hndl_Time())


	def save_series_local(self, regenerate=True):
		self.stored_series = self.__get_series(regenerate=regenerate)

	def __save_value_db(self, date, value, isInterpolated=False, isForecast=False):
		'''
		CONSIDER:
					Is it appropriate to cast values here? I think so....
		'''
		return lib_DBInst.insertDataPoint_DataHistoryTable( self._hndl_DB.conn, self._hndl_DB.cursor, 
															self.seriesID, 
															int(date), 
															float(value), 
															interpolated=int(isInterpolated),
															forecast=int(isForecast))

	def save_series_db(self, dates, values, isInterpolated=None, isForecast=None):
		'''
		TODOS: 
					Figure out what format dates, values, should come in [numpy array vs int] (to avoid weird casting errors)
					Store Data on successful inserts, maxDateEncountered, etc.
							What are we doing with dates we find?
		'''
		len_ = len(dates)		
		assert dates.shape == values.shape
		hasInt = (isInterpolated is not None)
		hasFor = (isForecast is not None)
		if hasInt:
			assert dates.shape == isInterpolated.shape
		if hasFor:
			assert dates.shape == isForecast.shape
		successfulInserts = 0
		unsuccessfulInserts = 0
		minDate = self.get_earliest_date()
		if minDate is None: minDate = maxint
		maxDate = self.get_latest_date()
		if minDate is None: minDate = -maxint-1
		for i in xrange(len_):
			isInt = hasInt and isInterpolated[i]
			isFor = hasFor and isForecast[i]
			date = dates[i]
			success = self.__save_value_db(date, values[i], isInt, isFor)
			if not success:
				log.warning('Failed to Write Historical Data Point at %s for %s [value = %f]', self.seriesTicker, dates[i], values[i])
				unsuccessfulInserts += 1
			else:
				minDate = min(date, minDate) 
				maxDate = max(date, maxDate)
				successfulInserts +=1
		self.__reset_num_points()
		self.__set_latest_date(maxDate)
		self.__set_earliest_date(minDate)
		self.__set_last_update()
		log.info('Successfully/Unsuccessfully wrote %d/%d Historical Data Points for %s', successfulInserts, unsuccessfulInserts, self.seriesTicker)
		return (successfulInserts, unsuccessfulInserts)

	def get_num_points(self):
		if 'num_data_points' in self._metadataCache:
			return self._metadataCache['num_data_points']
		else:
			numPoints = lib_DBInst.getCompleteDataHistory_DataHistoryTable(self._hndl_DB.cursor, self.seriesID, selectCount=True)
			self.set_num_points(numPoints)
			return numPoints
			
	def set_num_points(self, numPoints):
		self._metadataCache['num_data_points'] = numPoints

	def __reset_num_points(self):
		try:
			del self._metadataCache['num_data_points']
		except KeyError:
			pass

	def get_periodicity(self):
		return typify(int, self.__get_from_DB('int_periodicity'))

	def get_categorical(self):
		return typify(bool, self.__get_from_DB('bool_data_is_categorical'))

	def get_latest_date(self):
		return typify(int, self.__get_from_DB('dt_max_data_date'))

	def get_earliest_date(self):
		return typify(int, self.__get_from_DB('dt_min_data_date'))

	def get_last_update(self):
		return typify(int, self.__get_from_DB('dt_last_updated_history'))

	def set_periodicity(self, periodicity):
		self.__send_to_DB('int_periodicity', periodicity)

	def set_categorical(self, categorical):
		self.__send_to_DB('bool_data_is_categorical', categorical)

	def __set_latest_date(self, maxDate):
		self.__send_to_DB('dt_max_data_date', maxDate)

	def __set_earliest_date(self, minDate):
		self.__send_to_DB('dt_min_data_date', minDate)

	def __set_last_update(self):
		self.lastUpdate = dt_now_as_epoch()
		self.__send_to_DB('dt_last_updated_history', self.lastUpdate)

