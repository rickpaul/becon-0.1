# TODOS:
#	save maxDateEncountered, minDateEncountered, etc.
#	we insert but we don't retrieve isInterpolated, isForecast
#	Find a way to make sure that data history date/times match up (create canonical dates fn)
#	Do we really want to enforce dataSeries unsetting?


import EMF_DatabaseInstructions as EM_DBInst
import logging 	as log
import numpy as np


class EMF_DataSeries_Handle:
	def __init__(self, db_connection, db_cursor):
		self.db_conn = db_connection
		self.db_curs = db_cursor
		self.dataSeriesID = None
		self.dataHistory = None

	def __getFromDB(self, columnName):
		return EM_DBInst.retrieve_DataSeriesMetaData(self.db_conn, self.db_curs, columnName, self.dataSeriesID)

	def __sendToDB(self, columnName, value):
		return EM_DBInst.update_DataSeriesMetaData(self.db_conn, self.db_curs, columnName, value, self.dataSeriesID)

	def setDataSeries(self, name=None, ticker=None, insertIfNot=True):
		assert self.dataSeriesID is None # Force reset before setting (Or new object)
		self.dataSeriesID = EM_DBInst.retrieve_DataSeriesID(	self.db_conn, self.db_curs, 
																dataName=name,
																dataTicker=ticker,
																insertIfNot=insertIfNot)
		self.dataName = name
		self.dataTicker = ticker
		return self.dataSeriesID

	def unsetDataSeries(self):
		self.dataHistory = None
		self.dataSeriesID = None
		self.dataName = None
		self.dataTicker = None

	def getDataHistory(self, dataType='float', saveHistoryLocal=True):
		'''

		TODOS:
		Save dtype as value in lib
		'''
		assert self.dataSeriesID is not None
		dataSeries = EM_DBInst.getCompleteDataHistory_DataHistoryTable(self.db_conn, self.db_curs, self.dataSeriesID)
		dtype = [('date', 'int'), ('value', dataType)]
		dataSeries = np.asarray(dataSeries, dtype=dtype)
		if saveHistoryLocal:
			self.dataHistory = dataSeries
		return dataSeries

	def insertDataPoint(self, date, value, isInterpolated=False, isForecast=False):
		'''
		CONSIDER:
		Is it appropriate to cast values here? I think so....
		'''
		return EM_DBInst.insertDataPoint_DataHistoryTable( 	self.db_conn, self.db_curs, 
															self.dataSeriesID, 
															int(date), 
															float(value), 
															interpolated=int(isInterpolated),
															forecast=int(isForecast))

	def insertDataHistory(self, dates, values, isInterpolated=None, isForecast=None):
		'''

		TODOS: 
		Figure out what format dates, values, should come in [numpy array vs int] (to avoid weird casting errors)
		Don't insert each row separately?
		Store Data on successful inserts, maxDateEncountered, etc.
		'''
		assert self.dataSeriesID is not None
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
		for i in range(dataLen):
			isInt = hasInt and isInterpolated[i]
			isFor = hasFor and isForecast[i]
			success = self.insertDataPoint(dates[i], values[i], isInt, isFor)
			if not success:
				log.warning('Failed to Write Historical Data Point at %s for %s [value = %f]', self.dataTicker, dates[i], values[i])
				unsuccessfulInserts += 1
			else:
				successfulInserts +=1

		log.info('Successfully/Unsuccessfully wrote %d/%d Historical Data Points for %s', successfulInserts, unsuccessfulInserts, self.dataTicker)
