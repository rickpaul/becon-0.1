# TODOS:
#	we insert but we don't retrieve isInterpolated, isForecast
#	Find a way to make sure that data history date/times match up (create canonical dates fn)
#	Implement json handle

# EMF 		From...Import
from 	lib_DataSeries	import 	DATE_COL, VALUE_COL, DATA_HISTORY_DTYPE
from 	lib_JSON		import 	JSONRepository, DATA_SERIES_TO_JSON
from 	template_SerialHandle 	import EMF_Serial_Handle
from	util_EMF		import 	dt_now_as_epoch, dt_epoch_to_str_YMD, dt_date_range_generator
# EMF 		Import...As
import 	lib_DBInstructions 	as 	lib_DBInst
# System 	Import...As
import 	logging 			as 	log
import 	numpy 				as 	np
# System 	From...Import
from 	sys 			import 	maxint
from 	json 			import 	dumps 	as json_dump

class EMF_DataSeries_Handle(EMF_Serial_Handle):
	def __init__(self, dbHandle, name=None, ticker=None, insertIfNot=False):
		self.hndl_DB = dbHandle
		self.stored_series = None
		self._metadataCache = {}
		self.seriesID = self.__set_data_series(name, ticker, insertIfNot)

	def __str__(self):
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

	def __set_data_series(self, name, ticker, insertIfNot):
		'''
		TODOS: 
					Move up the insertIfNot functionality out of this fn
		'''
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

	def __get_series(self, regenerate=False):
		# If Stored, Return
		if (self.stored_series is not None) and (not regenerate):
			return self.stored_series
		# If not Stored, Get Data from DB
		else:
			dataSeries = lib_DBInst.getCompleteDataHistory_DataHistoryTable(self.hndl_DB.cursor_(), self.seriesID)
			dataSeries = np.asarray(dataSeries, dtype=DATA_HISTORY_DTYPE)
			self.set_num_points(len(dataSeries))
			return dataSeries

	def get_series_values_filtered(self, minDte, maxDte):
		series = self.__get_series()
		filter_ = np.logical_and(series[DATE_COL]>=minDte, series[DATE_COL]<=maxDte)
		return np.reshape(series[filter_][VALUE_COL], (sum(filter_), 1))

	def get_series_dates_filtered(self, minDte, maxDte):
		series = self.__get_series()
		filter_ = np.logical_and(series[DATE_COL]>=minDte, series[DATE_COL]<=maxDte)
		return np.reshape(series[filter_][DATE_COL], (sum(filter_), 1))

	def get_series_values(self):
		'''
		TODOS:
					We have no way to retrieve whether is interpolated or is forecast
		'''
		return self.__get_series()[VALUE_COL]

	def get_series_dates(self):
		'''
		TODOS:
					We have no way to retrieve whether is interpolated or is forecast
		'''
		return self.__get_series()[DATE_COL]

	def save_series_local(self, regenerate=True):
		self.stored_series = self.__get_series(regenerate=regenerate)

	def __save_value_to_db(self, date, value, isInterpolated=False, isForecast=False):
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

	def save_series_to_db(self, dates, values, isInterpolated=None, isForecast=None):
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
			success = self.__save_value_to_db(date, values[i], isInt, isFor)
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
			numPoints = lib_DBInst.getCompleteDataHistory_DataHistoryTable(self.hndl_DB.cursor_(), self.seriesID, selectCount=True)
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
		return self.__typify(int, self.__get_from_DB('code_local_periodicity'))

	def get_categorical(self):
		return self.__typify(bool, self.__get_from_DB('bool_data_is_categorical'))

	def get_latest_date(self):
		return self.__typify(int, self.__get_from_DB('dt_max_data_date'))

	def get_earliest_date(self):
		return self.__typify(int, self.__get_from_DB('dt_min_data_date'))

	def get_last_update(self):
		return self.__typify(int, self.__get_from_DB('dt_last_updated_history'))

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

	def __typify(self, type_, value_):
		if value_ is None:
			return None
		if type_ == bool:
			return bool(int(value_))
		else:
			return type_(value_)

	def write_to_JSON(self):
		'''
		TODOS:
					Create JSON Util
		'''
		JSON = map(DATA_SERIES_TO_JSON, self.__get_series())
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
			raise NotImplementedError


