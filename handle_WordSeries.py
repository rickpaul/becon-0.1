# TODOS:

# EMF 		From...Import
from 	lib_WordSeries	 		import DATE_COL, VALUE_COL, WORD_HISTORY_DTYPE
from 	util_EMF				import dt_now_as_epoch
from 	util_WordSeries			import generate_Word_Series_name
# EMF 		Import...As
import lib_DBInstructions as lib_DBInst
# System 	Import...As
import logging 	as log
import numpy 	as np

class EMF_WordSeries_Handle:
	def __init__(self, dbHandle, dataHandle, transformationHandle):
		self.hndl_DB = dbHandle
		self.hndl_Data = dataHandle
		self.hndl_Trns = transformationHandle
		self.wordSeriesID = lib_DBInst.retrieve_WordSeriesID(	self.hndl_DB.conn_(), 
																self.hndl_DB.cursor_(), 
																str(self),
																insertIfNot=True)
		self.__send_to_DB('int_data_series_ID', self.hndl_Data.seriesID)
		self.__send_to_DB('int_transformation_hash', self.hndl_Trns.trnsCode)
		self.stored_values = None
		self.stored_dates = None

	def __str__(self):
		return generate_Word_Series_name(str(self.hndl_Data), str(self.hndl_Trns))

	def __get_from_DB(self, column):
		return lib_DBInst.retrieve_WordSeriesMetaData(self.hndl_DB.cursor_(), column, self.wordSeriesID)

	def __send_to_DB(self, column, value):
		return lib_DBInst.update_WordSeriesMetaData(self.hndl_DB.conn_(), self.hndl_DB.cursor_(), column, value, self.wordSeriesID)

	def __generate_words(self):
		data = self.hndl_Data.save_series_local()
		# len_ = self.hndl_Trns.transform_data_length(self.hndl_Data.get_num_points())
		values = self.hndl_Trns.transform_data(self.hndl_Data.get_series_values())
		len_ = len(values)
		values = np.reshape(values, (len_, 1))
		dates = self.hndl_Trns.transform_time(self.hndl_Data.get_series_dates())
		dates = np.reshape(dates, (len_, 1))
		return (values, dates)

	def __get_series_from_DB(self):
		'''
		CONSIDER:
					We should check for transformation complexity. 
						It may be quicker to not access the db and just regenerate.
		'''	
		series = lib_DBInst.getCompleteWordHistory_WordHistoryTable(self.hndl_DB.cursor_(), 
																	self.wordSeriesID)
		series = np.asarray(dtype=WORD_HISTORY_DTYPE)
		(len_, ) = wordSeries.shape
		values = np.reshape(series[VALUE_COL], (len_, 1))
		dates = np.reshape(series[DATE_COL], (len_, 1))
		return (values, dates)

	def __get_series(self, regenerate=False):
		# If stored, Retrieve Words from DB
		if self.__get_word_is_in_db() and (not regenerate):
			return self.__get_series_from_DB()
		# If not stored, Generate Words
		else:
			return self.__generate_words()

	def get_series_values_filtered(self, minDte, maxDte):
		(values, dates) = self.__get_series()
		filter_ = np.logical_and(dates>minDte, dates<maxDte)
		return np.reshape(values[filter_], (sum(filter_), 1))

	def get_series_dates_filtered(self, minDte, maxDte):
		(values, dates) = self.__get_series()
		filter_ = np.logical_and(dates>minDte, dates<maxDte)
		return np.reshape(dates[filter_], (sum(filter_), 1))

	def get_series_values(self):
		self.__set_last_accessed()
		if self.stored_values is not None:
			return self.stored_values
		else:
			(values, dates) = self.__get_series()
			return values

	def get_series_dates(self):
		if self.stored_dates is not None:
			return self.stored_dates
		else:
			(values, dates) = self.__get_series()
			return dates

	def save_series_local(self, regenerate=False):
		(self.stored_values, self.stored_dates) = self.__get_series(regenerate=regenerate)

	def __save_value_to_db(self, date, value):
		'''
		TODOS: 
					- Make a version that takes more than one value (i.e. don't have to call this repeatedly.)
		'''
		return lib_DBInst.insertWordPoint_WordHistoryTable( self.hndl_DB.conn_(), 
															self.hndl_DB.cursor_(), 
															self.wordSeriesID, 
															date, 
															value)

	def save_series_to_db(self):
		'''

		TODOS: 
					++ Deal with None values
					++ Make roll back non-automatic 
					+ Store Data on successful inserts, maxDateEncountered, etc.
		'''
		(values, dates) = self.__get_series(regenerate=True)
		successfulInserts = 0
		unsuccessfulInserts = 0
		for i in xrange(dataLen):
			success = self.__save_value_to_db(dates[i], values[i])
			if not success:
				log.warning('Failed to Write Historical Word Point at %s for %s [value = %f]', self.wordSeriesTicker, dates[i], values[i])
				unsuccessfulInserts += 1
				break
			else:
				successfulInserts +=1
		# Roll Back Insert If Necessary
		if unsuccessfulInserts == 0:
			self.__set_word_is_stored(True)
		else:
			self.delete_word_history()
		log.info('Successfully/Unsuccessfully wrote %d/%d Historical Word Points for %s', successfulInserts, unsuccessfulInserts, self.wordSeriesTicker)
		return (successfulInserts, unsuccessfulInserts)

	def __typify(self, type_, value_):
		if value_ is None:
			return None
		if type_ == bool:
			return bool(int(value_))
		else:
			return type_(value_)

	def __set_last_accessed(self):
		self.__send_to_DB('dt_history_last_accessed', dt_now_as_epoch())

	def __set_word_is_stored(self, isStored):
		self.__send_to_DB('bool_word_is_stored', int(isStored))

	def __get_word_is_in_db(self):
		self.__typify(bool, self.__get_from_DB('bool_word_is_stored'))

	def get_model_categorization(self):
		if self.hndl_Data.get_categorical():
			if self.hndl_Trns.is_bounded:
				return 'categorical_bounded'
			else:
				return 'categorical_unbounded'
		else:
			return 'continuous'

	def get_earliest_word_date(self):
		minDte = self.hndl_Data.get_earliest_date()
		periodicity = self.hndl_Data.get_periodicity()
		return self.hndl_Trns.transform_earliest_time(minDte, periodicity)

	def get_latest_word_date(self):
		maxDte = self.hndl_Data.get_latest_date()
		periodicity = self.hndl_Data.get_periodicity()
		return self.hndl_Trns.transform_latest_time(maxDte, periodicity)

	def get_data_periodicity(self):
		return self.hndl_Data.get_periodicity()

	def get_data_ID(self):
		return self.hndl_Data.seriesID

	def get_data_Ticker(self):
		return self.hndl_Data.seriesTicker

	def delete_word_history(self):
		'''
		deletes word history from Database
		'''
		raise NotImplementedError
		self.__send_to_DB(self, 'bool_word_is_stored', 0)
		log.info('Deleting Word History for %s', self.wordSeriesTicker)

	def check_word_alignment(self, otherWordHandle):
		return np.all(self.get_series_dates() == otherWordHandle.get_series_dates())

