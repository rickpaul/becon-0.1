# EMF 		From...Import
from handle_DataSeries	 	import EMF_DataSeries_Handle
from handle_WordSeries 		import EMF_WordSeries_Handle
from lib_EMF		 		import TEMP_MODE
from util_CreateDB	 		import create_DB
from util_Logging	 		import init_logging
# EMF 		Import...As
# System 	Import...As
import logging 	as log
# System 	From...Import
from os import remove

class EMF_Testing_Handle:
	def __init__(self, mode=TEMP_MODE):
		(self.logLoc, self.deleteLog) = init_logging(mode=mode)
		self.hndl_DB = create_DB(mode=mode)
		self.wordHandles = {}

	def __del__(self):
		del self.hndl_DB
		if self.deleteLog:
			log.warning('Log File {} deleted'.format(self.logLoc))
			remove(self.logLoc)
		else:
			log.info('Log File stored in {}'.format(self.logLoc))

	def insert_test_data(self, dates, dataSet, dataTickers):
		dataHandle = EMF_DataSeries_Handle(self.hndl_DB)
		for (idx, ticker) in enumerate(dataTickers):
			try:
				values = dataSet[:,idx]
			except IndexError:
				values = dataSet
			dataHandle.set_data_series(name=ticker, ticker=ticker, insertIfNot=True)
			dataHandle.insert_data_history(dates, values)
			dataHandle.unset_data_series()

	def create_word_from_data(self, dataTicker, transformationPattern):
		wordHandle = EMF_WordSeries_Handle(self.hndl_DB, transformationPattern)
		dataHandle = EMF_DataSeries_Handle(self.hndl_DB)
		wordHandle.set_data_series(ticker=dataTicker)
		self.wordHandles[str(wordHandle)] = wordHandle
		return str(wordHandle)

	def retrieve_word(self, wordName):
		return self.wordHandles[wordName]