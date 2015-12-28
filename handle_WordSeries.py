# TODOS:

# EMF 		From...Import
from 	lib_WordSeries	 		import DATE_COL, VALUE_COL, WORD_HISTORY_DTYPE
from 	lib_DataSeries	 		import DATE_COL as DATA_DATE_COL
from 	lib_DataSeries	 		import VALUE_COL as DATA_VALUE_COL
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
																self.hndl_Data.seriesID,
																self.hndl_Trns.transformationCode,
																insertIfNot=True)
		self.stored_words = None
		self.stored_dates = None

	def __str__(self):
		return generate_Word_Series_Name(self.hndl_Data.seriesTicker, self.hndl_Trns.transformationName)

	def __get_from_DB(self, column):
		return lib_DBInst.retrieve_WordSeriesMetaData(self.hndl_DB.cursor_(), column, self.wordSeriesID)

	def __send_to_DB(self, column, value):
		return lib_DBInst.update_WordSeriesMetaData(self.hndl_DB.conn_(), self.hndl_DB.cursor_(), column, value, self.wordSeriesID)

	def check_word_alignment(self, otherWordHandle):
		return np.all(self.get_date_series == otherWordHandle.get_date_series)


	def __generate_words(self):
		data = self.hndl_Data.get_data_history()
		(dataLen, ) = data.shape
		words = np.reshape(self.hndl_Trns.transform_data(data[DATA_VALUE_COL]), (dataLen, 1))
		dates = np.reshape(self.hndl_Trns.transform_time(data[DATA_DATE_COL]), (dataLen, 1))
		return (words, dates)

	def __from_DB_get_word_series(self):
		wordSeries = lib_DBInst.getCompleteWordHistory_WordHistoryTable(self.hndl_DB.cursor_(), 
																		self.wordSeriesID)
		wordSeries = np.asarray(wordSeries, dtype=WORD_HISTORY_DTYPE)
		(dataLen, ) = wordSeries.shape
		words = np.reshape(wordSeries[VALUE_COL], (dataLen, 1))
		dates = np.reshape(wordSeries[DATE_COL], (dataLen, 1))
		return (words, dates)

	def get_word_series(self, saveHistoryLocal=False):
		'''
		PARAMETERS:
					<bool> saveHistoryLocal | tells whether to save the history internally
		TODOS:
		'''
		assert self.wordSeriesID is not None
		self.__send_to_DB('dt_history_last_accessed', dt_now_as_epoch())
		if self.stored_words is not None:
			return self.stored_words
		else:
			# If stored, Retrieve Words from DB
			if self.__get_from_DB('bool_word_is_stored'): 
				(words, dates) = self.__from_db_get_word_series()
			# If not stored, Generate Words
			else: 
				(words, dates) = self.__generate_words()
			if saveHistoryLocal:
				self.stored_words = words
				self.stored_dates = dates
			return words

	def get_date_series(self, saveHistoryLocal=False):
		'''
		PARAMETERS:
					<bool> saveHistoryLocal | tells whether to save the history internally
		TODOS:
		'''
		assert self.wordSeriesID is not None
		if self.stored_dates is not None:
			return self.stored_dates
		else:
			if self.__get_from_DB('bool_word_is_stored'): #Retrieve Words from DB
				(words, dates) = self.__from_db_get_word_series()
			else: # Generate Words
				(words, dates) = self.__generate_words()
			if saveHistoryLocal:
				self.stored_words = words
				self.stored_dates = dates
			return dates

	def __insert_word_point(self, date, value):
		'''
		TODOS: 
					- Make a version that takes more than one value (i.e. don't have to call this repeatedly.)
		'''
		assert self.wordSeriesID is not None
		return lib_DBInst.insertWordPoint_WordHistoryTable( self.hndl_DB.conn_(), 
															self.hndl_DB.cursor_(), 
															self.wordSeriesID, 
															date, 
															value)

	def insert_word_history(self, dates, values):
		'''

		TODOS: 
					++ Deal with None values
					++ Make roll back non-automatic 
					+ Store Data on successful inserts, maxDateEncountered, etc.
		'''
		assert self.wordSeriesID is not None
		(dataLen, dataWidth) = values.shape
		assert dataWidth 	== 1
		assert dates.shape 	== values.shape
		successfulInserts = 0
		unsuccessfulInserts = 0
		for i in xrange(dataLen):
			success = self.__insert_word_point(dates[i], values[i])
			if not success:
				log.warning('Failed to Write Historical Word Point at %s for %s [value = %f]', self.wordSeriesTicker, dates[i], values[i])
				unsuccessfulInserts += 1
			else:
				successfulInserts +=1
		# Roll Back Insert If Necessary
		if unsuccessfulInserts == 0:
			self.__send_to_DB('bool_word_is_stored', 1)
		else:
			self.deleteWordHistory()
		log.info('Successfully/Unsuccessfully wrote %d/%d Historical Word Points for %s', successfulInserts, unsuccessfulInserts, self.wordSeriesTicker)
		return (successfulInserts, unsuccessfulInserts)


	# def delete_word_history(self):
	# 	'''
	# 	deletes word history from Database
	# 	'''
	# 	raise NotImplementedError
	# 	assert self.wordSeriesID is not None
	# 	self.__send_to_DB(self, 'bool_word_is_stored', 0)
	# 	log.info('Deleting Word History for %s', self.wordSeriesTicker)

