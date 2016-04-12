# TODOS:
#	we insert but we don't retrieve isInterpolated, isForecast



# EMF 		From...Import
from 	handle_TimeSet 			import EMF_TimeSet_Handle, verify_date_series
from 	lib_DataSeries			import DATE_COL, VALUE_COL, DATA_HISTORY_DTYPE
# from 	template_SerialHandle 	import EMF_Serial_Handle
from 	util_DB					import typify
from	util_TimeSet			import dt_now_as_epoch
# EMF 		Import...As
import 	lib_DBInstructions 		as lib_DBInst
# System 	Import...As
import 	logging 				as log
import 	numpy 					as np
# System 	From...Import
from 	sys 					import maxint

class EMF_DataSeries_Handle(object):
	def __init__(self, dbHandle, name=None, ticker=None, insertIfNot=False):
		'''
		CONSIDER:
					Make periodicity a required field for insertion? (NO.)
		'''
		self._hndl_DB = dbHandle
		self._hndl_Time = None
		self.stored_series = None
		self._metadataCache = {}
		self._seriesID = lib_DBInst.retrieve_DataSeriesID(	self._hndl_DB.conn, 
															self._hndl_DB.cursor,
															name=name,
															ticker=ticker,
															insertIfNot=insertIfNot)
		assert self._seriesID is not None # Did we catch something?
		if name is None: name = self.__load_metadata('txt_data_name')
		self._name = name
		if ticker is None: ticker = self.__load_metadata('txt_data_ticker')
		self._ticker = ticker

	def __str__(self):
		return self.ticker
		
	def seriesID():
		doc = "The seriesID property."
		def fget(self):
			return self._seriesID
		return locals()
	seriesID = property(**seriesID())

	def name():
		doc = "The name property."
		def fget(self):
			return self._name
		return locals()
	name = property(**name())

	def ticker():
		doc = "The ticker property."
		def fget(self):
			return self._ticker
		return locals()
	ticker = property(**ticker())	

	def last_refreshed():
		doc = "The last_refreshed property."
		def fget(self):
			return typify(int, self.__load_metadata('dt_last_refreshed_date'))
		def fset(self, value):
			self.__save_metadata('dt_last_refreshed_date', value)
		return locals()
	last_refreshed = property(**last_refreshed())

	def geography():
		doc = "The geography property."
		def fget(self):
			return typify(str, self.__load_metadata('txt_geography'))
		def fset(self, value):
			self.__save_metadata('txt_geography', value)
		return locals()
	geography = property(**geography())

	def category():
		doc = "The category property."
		def fget(self):
			return typify(str, self.__load_metadata('txt_category'))
		def fset(self, value):
			self.__save_metadata('txt_category', value)
		return locals()
	category = property(**category())

	def subcategory():
		doc = "The subcategory property."
		def fget(self):
			return typify(str, self.__load_metadata('txt_subcategory'))
		def fset(self, value):
			self.__save_metadata('txt_subcategory', value)
		return locals()
	subcategory = property(**subcategory())

	def category_meaning():
		doc = "The category_meaning property."
		def fget(self):
			return typify(str, self.__load_metadata('txt_category_meaning'))
		def fset(self, value):
			self.__save_metadata('txt_category_meaning', value)
		return locals()
	category_meaning = property(**category_meaning())

	def max_date():
		doc = "The max_date property."
		def fget(self):
			return typify(int, self.__load_metadata('dt_max_data_date'))
		def fset(self, value):
			self.__save_metadata('dt_max_data_date', value)
		return locals()
	max_date = property(**max_date())

	def min_date():
		doc = "The min_date property."
		def fget(self):
			return typify(int, self.__load_metadata('dt_min_data_date'))
		def fset(self, value):
			self.__save_metadata('dt_min_data_date', value)
		return locals()
	min_date = property(**min_date())

	def is_categorical():
		doc = "The is_categorical property."
		def fget(self):
			return typify(bool, self.__load_metadata('bool_data_is_categorical'))
		def fset(self, value):
			self.__save_metadata('bool_data_is_categorical', value)
		return locals()
	is_categorical = property(**is_categorical())

	def periodicity():
		doc = "The periodicity property."
		def fget(self):
			return typify(int, self.__load_metadata('code_local_periodicity'))
		def fset(self, value):
			self.__save_metadata('code_local_periodicity', value)
		return locals()
	periodicity = property(**periodicity())
	
	def original_periodicity():
		doc = "The original_periodicity property."
		def fget(self):
			return typify(int, self.__load_metadata('code_original_periodicity'))
		def fset(self, value):
			self.__save_metadata('code_original_periodicity', value)
		return locals()
	original_periodicity = property(**original_periodicity())

	def last_update():
		doc = "The last_update property."
		def fget(self):
			return typify(int, self.__load_metadata('dt_last_updated_history'))
		return locals()
	last_update = property(**last_update())

	def Quandl_dataset():
		doc = "The Quandl_dataset property."
		def fget(self):
			return typify(int, self.__load_metadata('txt_Quandl_dataset'))
		def fset(self, value):
			self.__save_metadata('txt_Quandl_dataset', value)
		return locals()
	Quandl_dataset = property(**Quandl_dataset())

	def Quandl_database():
		doc = "The Quandl_database property."
		def fget(self):
			return typify(int, self.__load_metadata('txt_Quandl_database'))
		def fset(self, value):
			self.__save_metadata('txt_Quandl_database', value)
		return locals()
	Quandl_database = property(**Quandl_database())

	def __set_last_update(self):
		self.__save_metadata('dt_last_updated_history', dt_now_as_epoch())

	def __load_metadata(self, column):
		if column in self._metadataCache:
			return self._metadataCache[column]
		value = lib_DBInst.retrieve_DataSeriesMetaData(self._hndl_DB.cursor, column, self.seriesID)
		self._metadataCache[column] = value
		return value

	def __save_metadata(self, column, value):
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
			# self.set_num_points(len(dataSeries))
			return dataSeries

	def dates():
		doc = "The dates property."
		def fget(self):
			return self.get_series_dates()
		return locals()
	dates = property(**dates())

	def values():
		doc = "The values property."
		def fget(self):
			return self.get_series_values()
		return locals()
	values = property(**values())

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
				self._hndl_Time.periodicity = self.periodicity
				self._hndl_Time.startEpoch = self.min_date
				self._hndl_Time.endEpoch = self.max_date
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
					Store Data on successful inserts, max_Encountered, etc.
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
		min_ = self.min_date
		if min_ is None: min_ = maxint
		max_ = self.max_date
		if max_ is None: max_ = -maxint-1
		for i in xrange(len_):
			isInt = hasInt and isInterpolated[i]
			isFor = hasFor and isForecast[i]
			date = dates[i]
			success = self.__save_value_db(date, values[i], isInt, isFor)
			if not success:
				log.warning('Failed to Write Historical Data Point at %s for %s [value = %f]', self.ticker, dates[i], values[i])
				unsuccessfulInserts += 1
			else:
				min_ = min(date, min_) 
				max_ = max(date, max_)
				successfulInserts +=1
		# self.__reset_num_points()
		self.max_date = max_
		self.min_date = min_
		self.__set_last_update()
		log.info('Successfully/Unsuccessfully wrote %d/%d Historical Data Points for %s', successfulInserts, unsuccessfulInserts, self.ticker)
		return (successfulInserts, unsuccessfulInserts)

	# def get_num_points(self):
	# 	if 'num_data_points' in self._metadataCache:
	# 		return self._metadataCache['num_data_points']
	# 	else:
	# 		numPoints = lib_DBInst.getCompleteDataHistory_DataHistoryTable(self._hndl_DB.cursor, self.seriesID, selectCount=True)
	# 		self.set_num_points(numPoints)
	# 		return numPoints
			
	# def set_num_points(self, numPoints):
	# 	self._metadataCache['num_data_points'] = numPoints

	# def __reset_num_points(self):
	# 	try:
	# 		del self._metadataCache['num_data_points']
	# 	except KeyError:
	# 		pass

	# def get_series_values_filtered(self, min_, max_):
	# 	series = self.__get_series()
	# 	filter_ = np.logical_and(series[DATE_COL]>=min_, series[DATE_COL]<=max_)
	# 	return np.reshape(series[filter_][VALUE_COL], (sum(filter_), 1))

	# def get_series_dates_filtered(self, min_, max_):
	# 	series = self.__get_series()
	# 	filter_ = np.logical_and(series[DATE_COL]>=min_, series[DATE_COL]<=max_)
	# 	return np.reshape(series[filter_][DATE_COL], (sum(filter_), 1))

