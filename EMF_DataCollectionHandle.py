DEPRECATED! DELETE!!!!

# # TODO:
# # Rename as DataSeriesHandle

# import EMF_DatabaseInstructions as EM_DBInst
# import logging 	as log


# class EMF_DataCollection_Handle:
# 	def __init__(self, db_connection, db_cursor):
# 		self.db_conn = db_connection
# 		self.db_curs = db_cursor
# 		self.dataSeriesID = None
# 		# TODO: Save maxDateEncountered, minDateEncountered, etc.

# 	def getFromDB(self, columnName):
# 		return EM_DBInst.retrieve_DataSeriesMetaData(self.db_conn, self.db_curs, columnName, seriesID=self.dataSeriesID)

# 	def sendToDB(self, columnName, value):
# 		return EM_DBHelp.update_DataSeriesMetaData(self.db_conn, self.db_curs, columnName, value, seriesID=self.dataSeriesID)

# 	def setDataSeries(self, name=None, ticker=None, insertIfNot=True):
# 		assert self.dataSeriesID is None # Force reset before setting (Or new object)

# 		self.dataSeriesID = EM_DBInst.retrieve_DataSeriesID(	self.db_conn, self.db_curs, 
# 																dataName=name,
# 																dataTicker=ticker,
# 																insertIfNot=insertIfNot)
# 		self.dataName = name
# 		self.dataTicker = ticker

# 	def unsetDataSeries(self):
# 		self.dataSeriesID = None
# 		self.dataName = None
# 		self.dataTicker = None

# 	def getDataHistory(self, dataType='float'):
# 		'''
# 		'''
# 		assert self.dataSeriesID is not None
# 		dataSeries = EM_DBInst.retrieve_DataSeriesID(self.db_conn, self.db_curs, self.dataSeriesID)
# 		dtype = [('date', 'int'), ('value', dataType)]
# 		dataSeries = np.asarray(dataSeries, dtype=dtype)
# 		return dataSeries

# 	def insertDataPoint(self, date, value, isInterpolated=False, isForecast=False):
# 		'''
# 		'''
# 		return EM_DBInst.insertDataPoint_DataHistoryTable( 	self.db_conn, self.db_curs, 
# 															self.dataSeriesID, 
# 															date, 
# 															value, 
# 															interpolated=isInterpolated,
# 															forecast=isForecast)

# 	def insertDataHistory(self, dates, values, isInterpolated=None, isForecast=None):
# 		'''

# 		TODOS: 
# 		Don't insert each row separately.
# 		Store Data on successful inserts, maxDateEncountered, etc.
# 		'''
# 		assert self.dataSeriesID is not None
# 		dataLen = len(dates)
# 		assert dates.shape == values.shape
# 		hasInt = (isInterpolated is not None)
# 		hasFor = (isForecast is not None)
# 		if hasInt:
# 			assert dates.shape == isInterpolated.shape
# 		if hasFor:
# 			assert dates.shape == isForecast.shape
# 		successfulInserts = 0
# 		unsuccessfulInserts = 0
# 		for i in range(dataLen):
# 			isInt = hasInt and isInterpolated[i]
# 			isFor = hasFor and isForecast[i]
# 			success = self.insertDataPoint(dates[i], values[i], isInt, isFor)
# 			if not success:
# 				log.warning('Failed to Write Historical Data Point at %s for %s [value = %f]', dataSeriesTicker, dates[i], values[i])
# 				unsuccessfulInserts += 1
# 			else:
# 				successfulInserts +=1

# 		log.info('Successfully/Unsuccessfully wrote %d/%d Historical Data Points for %s', successfulInserts, unsuccessfulInserts, dataSeriesTicker)
