# TODOS:
#	Rename/Refactor Functions to underscore format

# EMF 		From...Import
from 	handle_DataSeries 		import EMF_DataSeries_Handle as DataHandle
from 	handle_Transformation 	import EMF_Transformation_Handle as TransformationHandle
from 	lib_Transformation 		import TRANS_P_GEOM_DIST, MAX_TRANSFORMATIONS, CommonTransformations
from 	lib_WordSeries	 		import DATE_COL, VALUE_COL, WORD_HISTORY_DTYPE
from 	lib_DataSeries	 		import DATE_COL as DATA_DATE_COL
from 	lib_DataSeries	 		import VALUE_COL as DATA_VALUE_COL
from 	util_EMF				import dtGetNowAsEpoch
from 	util_WordSeries			import retrieve_WordHandle_from_Name
# EMF 		Import...As
import lib_DBInstructions as lib_DBInst
# System 	Import...As
import logging 	as log
# System 	From...Import
from 	numpy.random import geometric

class EMF_WordSeries_Handle:
	def __init__(self, dbHandle):
		self.hndl_DB = dbHandle
		self.hndl_Data = DataHandle(dbHandle)
		self.hndl_Trns = TransformationHandle()
		self.wordSeriesID = None
		self.wordHistory = None

	def __str__(self):
		return retrieve_WordHandle_from_Name(self.hndl_Data, self.hndl_Trns)

	def __get_from_DB(self, column):
		return lib_DBInst.retrieve_WordSeriesMetaData(self.hndl_DB.cursor_(), column, self.wordSeriesID)

	def __send_to_DB(self, column, value):
		return lib_DBInst.update_WordSeriesMetaData(self.hndl_DB.conn_(), self.hndl_DB.cursor_(), column, value, self.wordSeriesID)

	def __set_word_series(self):
		if (self.hndl_Trns.transformationCode is not None) and (self.hndl_Data.dataSeriesID is not None):
			self.wordSeriesID = lib_DBInst.retrieve_WordSeriesID(	self.hndl_DB.conn_(), 
																	self.hndl_DB.cursor_(), 
																	self.hndl_Data.dataSeriesID,
																	self.hndl_Trns.transformationCode,
																	insertIfNot=True)

	def __unset_word_series(self):
		self.wordSeriesID = None
		self.wordHistory = None
		self.wordIsCategorical = None

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
		return np.all(self.getWordHistory['dates'] == otherWordHandle.getWordHistory['dates'])

	def setTransformation_FromTemplate(self, trnsSeries):
		'''
		trnsSeries tuple<list<string>, string> is modeled off lib_Transformation.CommonTransformations
		'''
		# assert self.transformationHash is None # Force reset before setting (Or new object)
		(code, transList, categorization) = CommonTransformations[trnsSeries]
		for transformation in transList:
			self.hndl_Trns.addTransformation_named(transformation)
		self.hndl_Trns.setCategorization(categorization)
		# self.transformationHash = self.hndl_Trns.getTransformation_asHash()
		self.__set_word_series()

	def setTransformation_Random(self, numTransformations=None):
		'''
		'''
		if numTransformations is None: 
			numTransformations = min(MAX_TRANSFORMATIONS, geometric(.75))
		# assert self.transformationHash is None # Force reset before setting (Or new object)
		for i in xrange(numTransformations):
			self.hndl_Trns.addTransformation_random()
		self.hndl_Trns.randomizeCategorization()
		# self.transformationHash = self.hndl_Trns.getTransformation_asHash()
		self.__set_word_series()

	def unsetTransformation(self):
		# self.transformationHash = None
		self.hndl_Trns.unsetTransformationPattern()
		self.__unset_word_series()


	def getWordHistory(self, saveHistoryLocal=True):
		'''
		PARAMETERS:
					<bool> saveHistoryLocal | tells whether to save the history internally
		TODOS:
		'''
		assert self.wordSeriesID is not None
		self.__send_to_DB('dt_history_last_accessed', dtGetNowAsEpoch())
		if self.wordHistory is not None:
			return self.wordHistory
		else:
			isInDB = self.__get_from_DB('bool_word_is_stored')
			if isInDB: #Retrieve Words from DB
				wordSeries = lib_DBInst.getCompleteWordHistory_WordHistoryTable(self.hndl_DB.cursor_(), 
																				self.wordSeriesID)
				wordSeries = np.asarray(wordSeries, dtype=WORD_HISTORY_DTYPE)
			else: # Generate Words
				data = self.hndl_Data.getDataHistory()
				words = self.hndl_Trns.transformDataSeries(data[DATA_VALUE_COL])
				dates = self.hndl_Trns.transformTimeSeries(data[DATA_DATE_COL])
				wordSeries = np.asarray(np.hstack(words, dates), dtype=WORD_HISTORY_DTYPE)
			if saveHistoryLocal:
				self.wordHistory = wordSeries
			return wordSeries

	def __insert_word_point(self, date, value):
		'''
		'''
		assert self.wordSeriesID is not None
		return lib_DBInst.insertWordPoint_WordHistoryTable( self.hndl_DB.conn_(), 
															self.hndl_DB.cursor_(), 
															self.wordSeriesID, 
															date, 
															value)

	def insertWordHistory(self, dates, values):
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


	def deleteWordHistory(self):
		'''
		deletes word history from Database
		'''
		assert self.wordSeriesID is not None
		self.__send_to_DB(self, 'bool_word_is_stored', 0)
		log.info('Deleting Word History for %s', self.wordSeriesTicker)
		raise NotImplementedError

