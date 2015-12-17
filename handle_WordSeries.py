# TODOS:

# EMF 		From...Import
from 	handle_DataSeries 		import EMF_DataSeries_Handle as DataHandle
from 	handle_Transformation 	import EMF_Transformation_Handle as TransformationHandle
from 	lib_WordSeries	 		import DATE_COL, VALUE_COL, WORD_HISTORY_DTYPE
from 	lib_DataSeries	 		import DATE_COL as DATA_DATE_COL
from 	lib_DataSeries	 		import VALUE_COL as DATA_VALUE_COL
from 	util_EMF				import dtGetNowAsEpoch
# EMF 		Import...As
import lib_DBInstructions as lib_DBInst
# System 	Import...As
import logging 	as log
import numpy 	as np

class EMF_WordSeries_Handle:
	def __init__(self, dbHandle, transformationPattern):
		self.hndl_DB = dbHandle
		self.hndl_Data = DataHandle(dbHandle)
		self.hndl_Trns = TransformationHandle(transformationPattern)
		self.wordSeriesID = None
		self.stored_words = None
		self.stored_dates = None

	def __str__(self):
		return str(self.hndl_Data) + "|" + str(self.hndl_Trns)

	def __get_from_DB(self, column):
		return lib_DBInst.retrieve_WordSeriesMetaData(self.hndl_DB.cursor_(), column, self.wordSeriesID)

	def __send_to_DB(self, column, value):
		return lib_DBInst.update_WordSeriesMetaData(self.hndl_DB.conn_(), self.hndl_DB.cursor_(), column, value, self.wordSeriesID)

	def __set_word_series(self):
		if (self.hndl_Trns.transformationCode is not None) and (self.hndl_Data.seriesID is not None):
			self.wordSeriesID = lib_DBInst.retrieve_WordSeriesID(	self.hndl_DB.conn_(), 
																	self.hndl_DB.cursor_(), 
																	self.hndl_Data.seriesID,
																	self.hndl_Trns.transformationCode,
																	insertIfNot=True)

	def __unset_word_series(self):
		self.wordSeriesID = None
		self.stored_words = None
		self.stored_dates = None
		# self.wordIsCategorical = None

	def set_data_series(self, name=None, ticker=None):
		'''
		TODOS:
					Check and store if data series is categorical (matters for transformations)
		'''
		self.hndl_Data.set_data_series(	name=name,
										ticker=ticker,
										insertIfNot=False)
		self.__set_word_series()

	def unset_data_series(self):
		self.hndl_Data.unset_data_series()
		self.__unset_word_series()

	def check_word_alignment(self, otherWordHandle):
		return np.all(self.get_word_history['dates'] == otherWordHandle.get_word_history['dates'])

	def set_transformation(self, trnsSeries):
		'''
		trnsSeries tuple<list<string>, string> is modeled off lib_Transformation.CommonTransformations
		'''
		self.__set_word_series()

	def get_word_series(self, saveHistoryLocal=False):
		'''
		PARAMETERS:
					<bool> saveHistoryLocal | tells whether to save the history internally
		TODOS:
		'''
		assert self.wordSeriesID is not None
		self.__send_to_DB('dt_history_last_accessed', dtGetNowAsEpoch())
		if self.stored_words is not None:
			return self.stored_words
		else:
			if self.__get_from_DB('bool_word_is_stored'): #Retrieve Words from DB
				wordSeries = lib_DBInst.getCompleteWordHistory_WordHistoryTable(self.hndl_DB.cursor_(), 
																				self.wordSeriesID)
				wordSeries = np.asarray(wordSeries, dtype=WORD_HISTORY_DTYPE)
				(dataLen, ) = wordSeries.shape
				words = np.reshape(wordSeries, (dataLen, 1))
				dates = np.reshape(wordSeries, (dataLen, 1))
			else: # Generate Words
				data = self.hndl_Data.get_data_history()
				(dataLen, ) = data.shape
				words = np.reshape(self.hndl_Trns.transform_data(data[DATA_VALUE_COL]), (dataLen, 1))
				dates = np.reshape(self.hndl_Trns.transform_time(data[DATA_DATE_COL]), (dataLen, 1))
			if saveHistoryLocal:
				self.stored_words = words
				self.stored_dates = dates
			return words

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

