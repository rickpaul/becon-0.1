# TODOS:
#	we insert but we don't retrieve isInterpolated, isForecast
#	Find a way to make sure that data history date/times match up (create canonical dates fn)
#	Do we really want to allow dataSeries unsetting? Should make you delete object
#	Refactor [e.g. unset_data_series --> unset]
#		Implement template class for Handles?

# EMF 		From...Import
from	util_EMF		import 	dt_now_as_epoch, dt_epoch_to_str_YMD, dt_date_range_generator
from 	lib_DataSeries	import 	DATE_COL, VALUE_COL, DATA_HISTORY_DTYPE
from 	lib_JSON		import 	JSONRepository, DATA_SERIES_TO_JSON
# EMF 		Import...As
import 	lib_DBInstructions 	as 	lib_DBInst
# System 	Import...As
import 	logging 			as 	log
import 	numpy 				as 	np
# System 	From...Import
from 	sys 			import 	maxint
from 	json 			import 	dumps 	as json_dump

class EMF_DataSeries_Handle:
	def __init__(self, dbHandle):
		self.hndl_DB = dbHandle
		self.seriesID = None
		self._dataHistory = None
		self._metadataCache = {}

	def __str__(self):
		assert self.seriesID is not None
		return self.seriesTicker

	def __get_from_DB(self, column):
		if column in self._metadataCache:
			return self._metadataCache[column]
		value = lib_DBInst.retrieve_DataSeriesMetaData(self.hndl_DB.cursor_(), column, self.seriesID)
		self._metadataCache[column] = value
		return value

	def __send_to_DB(self, column, value):
		success = lib_DBInst.update_DataSeriesMetaData(self.hndl_DB.conn_(), self.hndl_DB.cursor_(), column, value, self.seriesID)
		if success:
			self._metadataCache[column] = value
		else:
			raise NotImplementedError #How 

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
		self._dataHistory = None
		self.seriesID = None
		self.seriesName = None
		self.seriesTicker = None

	def get_data_history(self, saveHistoryLocal=True):
		'''
		TODOS:
					We have no way to retrieve whether is interpolated or is forecast
		'''
		assert self.seriesID is not None
		dataSeries = lib_DBInst.getCompleteDataHistory_DataHistoryTable(self.hndl_DB.cursor_(), self.seriesID)
		dataSeries = np.asarray(dataSeries, dtype=DATA_HISTORY_DTYPE)
		if saveHistoryLocal:
			self._dataHistory = dataSeries
		return dataSeries

	def __write_data_point(self, date, value, isInterpolated=False, isForecast=False):
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

	def write_to_DB(self, dates, values, isInterpolated=None, isForecast=None, saveHistoryLocal=True):
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
		minDate = self.get_earliest_date()
		if minDate is None: minDate = maxint
		maxDate = self.get_latest_date()
		if minDate is None: minDate = -maxint-1
		for i in range(dataLen):
			isInt = hasInt and isInterpolated[i]
			isFor = hasFor and isForecast[i]
			date = dates[i]
			success = self.__write_data_point(date, values[i], isInt, isFor)
			if not success:
				log.warning('Failed to Write Historical Data Point at %s for %s [value = %f]', self.seriesTicker, dates[i], values[i])
				unsuccessfulInserts += 1
			else:
				minDate = min(date, minDate) 
				maxDate = max(date, maxDate)
				successfulInserts +=1
		self.__set_latest_date(maxDate)
		self.__set_earliest_date(minDate)
		self.__set_last_update()
		log.info('Successfully/Unsuccessfully wrote %d/%d Historical Data Points for %s', successfulInserts, unsuccessfulInserts, self.seriesTicker)
		if saveHistoryLocal:
			self._dataHistory = np.asarray(np.hstack((dates, values)), dtype=DATA_HISTORY_DTYPE)
		return (successfulInserts, unsuccessfulInserts)

	def get_num_data_points(self):
		raise NotImplementedError

	def get_periodicity(self):
		return self.__typify(int, self.__get_from_DB('int_periodicity'))

	def get_categorical(self):
		return self.__typify(bool, self.__get_from_DB('bool_data_is_categorical'))

	def get_latest_date(self):
		return self.__typify(int, self.__get_from_DB('dt_max_data_date'))

	def get_earliest_date(self):
		return self.__typify(int, self.__get_from_DB('dt_min_data_date'))

	def get_last_update(self):
		return self.__typify(int, self.__get_from_DB('dt_last_updated_history'))

	def __typify(self, type_, value_):
		if value_ is None:
			return None
		if type_ == bool:
			return bool(int(value_))
		else:
			return type_(value_)

	def set_periodicity(self, periodicity):
		self.__send_to_DB('int_periodicity', periodicity)

	def set_categorical(self, categorical):
		self.__send_to_DB('bool_data_is_categorical', categorical)

	def __set_latest_date(self, maxDate):
		'''
		TODO:
					Send back True/False based on if new minDate is set
		'''
		self.__send_to_DB('dt_max_data_date', maxDate)

	def __set_earliest_date(self, minDate):
		'''
		TODO:
					Send back True/False based on if new minDate is set
		'''
		self.__send_to_DB('dt_min_data_date', minDate)

	def __set_last_update(self):
		self.lastUpdate = dt_now_as_epoch()
		self.__send_to_DB('dt_last_updated_history', self.lastUpdate)

	def write_to_JSON(self):
		'''
		TODOS:
					Create JSON Util
		'''
		if self._dataHistory is None:
			self.get_data_history(saveHistoryLocal=True)
		JSON = map(DATA_SERIES_TO_JSON, self._dataHistory)
		JSONFileName = self.__get_JSON_filename()
		try:
			writer = open(JSONFileName, 'wb')
			writer.write(json_dump(JSON))
		except:
			raise
		finally:
			writer.close()

	def __get_JSON_filename(self, simple=True):		
		fileName = self.seriesTicker
		if not simple:
			fileName += ('|' + dt_epoch_to_str_YMD(self.get_earliest_date()))
			fileName += ('|' + dt_epoch_to_str_YMD(self.get_latest_date()))
			fileName += ('|' + dt_epoch_to_str_YMD(self.get_last_update()))
		return (JSONRepository + fileName + '.json')

	def check_data_fullness(self, periodicity=12):
		'''
		This method checks if the data is filled in (i.e. if data is monthly since 1990, 
			every year should have) 12 points at expected times.
		'''
		generator = dt_date_range_generator(self.get_earliest_date(), self.get_latest_date(), periodicity)

		if periodicity == 12:
			self.get_data_history()
		else:
			raise NotImplementedError


