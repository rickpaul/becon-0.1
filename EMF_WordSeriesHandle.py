# TODO:
#	Find a way to make sure that word history date/times match up

from 	numpy.random import geometric

from 	EMF_DataSeriesHandle 		import EMF_DataSeries_Handle as DataHandle
from 	EMF_TransformationHandle 	import EMF_Transformation_Handle as TrnsHandle
from 	EMF_Transformations_lib 	import TRANS_P_GEOM_DIST, CommonTransformations
from 	EMF_util					import dtGetNowAsEpoch

import EMF_DatabaseInstructions as EM_DBInst

import logging 	as log


class EMF_WordSeries_Handle:
	def __init__(self, db_connection, db_cursor):
		self.db_conn = db_connection
		self.db_curs = db_cursor
		self.DataSeriesHandle = DataHandle(db_connection, db_cursor)
		self.TransformationHandle = TrnsHandle()
		self.dataSeriesID = None
		self.transformationHash = None
		self.wordSeriesID = None
		self.wordHistory = None
		self.timeHistory = None

	def __getFromDB(self, columnName):
		return EM_DBInst.retrieve_WordSeriesMetaData(self.db_conn, self.db_curs, columnName, self.wordSeriesID)

	def __sendToDB(self, columnName, value):
		return EM_DBInst.update_WordSeriesMetaData(self.db_conn, self.db_curs, columnName, value, self.wordSeriesID)

	def __setWordSeries(self):
		if (self.transformationHash is not None) and (self.dataSeriesID is not None):
			self.wordSeriesID = EM_DBInst.retrieve_WordSeriesID(	self.db_conn, self.db_curs, 
																self.dataSeriesID,
																self.transformationHash,
																insertIfNot=True)

	def __unsetWordSeries(self):
		self.wordSeriesID = None
		self.wordHistory = None
		self.timeHistory = None

	def setDataSeries(self, name=None, ticker=None):
		assert self.dataSeriesID is None # Force reset before setting (Or new object)
		self.dataSeriesID = self.DataSeriesHandle.setDataSeries(name=name,
																ticker=ticker,
																insertIfNot=False)

		self.__setWordSeries()

	def unsetDataSeries(self):
		self.dataSeriesID = None
		self.DataSeriesHandle.unsetDataSeries()
		self.__unsetWordSeries()

	def setTransformation_FromTemplate(self, trnsSeries):
		'''
		trnsSeries tuple<list<string>, string> is modeled off EMF_Transformations_lib.CommonTransformations
		'''
		assert self.transformationHash is None # Force reset before setting (Or new object)
		(transList, categorization) = CommonTransformations[trnsSeries]
		for transformation in transList:
			self.TransformationHandle.addTransformation_named(transformation)
		self.TransformationHandle.setCategorization(categorization)
		self.transformationHash = self.TransformationHandle.getTransformation_asHash()
		self.__setWordSeries()

	def setTransformation_Random(self, numTransformations=geometric(.75)):
		'''
		'''
		assert self.transformationHash is None # Force reset before setting (Or new object)
		for i in xrange(numTransformations):
			self.TransformationHandle.addTransformation_random()
		self.TransformationHandle.randomizeCategorization()
		self.transformationHash = self.TransformationHandle.getTransformation_asHash()
		self.__setWordSeries()

	def unsetTransformation(self):
		self.transformationHash = None
		self.TransformationHandle.unsetTransformationPattern()
		self.__unsetWordSeries()


	def getWordHistory(self, dataType='float', saveHistoryLocal=True):
		'''
		saveHistoryLocal bool tells whether to save the history internally
		TODOS:
		Save dtype as value in lib
		'''
		assert self.wordSeriesID is not None
		self.__sendToDB('dt_history_last_accessed', dtGetNowAsEpoch())
		if self.wordHistory is not None:
			return self.wordHistory
		else:
			isInDB = self.__getFromDB('bool_word_is_stored')
			if isInDB: #Retrieve Words from DB
				wordSeries = EM_DBInst.getCompleteWordHistory_WordHistoryTable(self.db_conn, self.db_curs, self.wordSeriesID)
				dtype = [('date', 'int'), ('value', dataType)]
				wordSeries = np.asarray(wordSeries, dtype=dtype)
			else: # Generate Words
				dataSeries = self.DataSeriesHandle.getDataHistory()
				wordSeries = self.TransformationHandle.transformDataSeries(dataSeries['value'])
				timeSeries = self.TransformationHandle.transformTimeSeries(dataSeries['date'])
			if saveHistoryLocal:
				self.wordHistory = wordSeries
				self.timeHistory = timeSeries
			return (wordSeries, timeSeries)

	def insertWordPoint(self, date, value):
		'''
		'''
		assert self.wordSeriesID is not None
		return EM_DBInst.insertWordPoint_WordHistoryTable( 	self.db_conn, self.db_curs, 
															self.wordSeriesID, 
															date, 
															value)

	def insertWordHistory(self, dates, values):
		'''

		TODOS: 
		Don't insert each row separately?
		Store Data on successful inserts, maxDateEncountered, etc.

		'''
		assert self.wordSeriesID is not None
		dataLen = len(dates)
		assert dates.shape == values.shape
		successfulInserts = 0
		unsuccessfulInserts = 0
		for i in xrange(dataLen):
			success = self.insertWordPoint(dates[i], values[i])
			if not success:
				log.warning('Failed to Write Historical Word Point at %s for %s [value = %f]', self.wordSeriesTicker, dates[i], values[i])
				unsuccessfulInserts += 1
			else:
				successfulInserts +=1

		# Roll Back Insert If Necessary
		if unsuccessfulInserts == 0:
			self.__sendToDB('bool_word_is_stored', 1)
		else:
			self.deleteWordHistory()
		
		log.info('Successfully/Unsuccessfully wrote %d/%d Historical Word Points for %s', successfulInserts, unsuccessfulInserts, self.wordSeriesTicker)


	def deleteWordHistory(self):
		assert self.wordSeriesID is not None
		self.__sendToDB(self, 'bool_word_is_stored', 0)
		log.info('Deleting Word History for %s', self.wordSeriesTicker)
		raise NotImplementedError

