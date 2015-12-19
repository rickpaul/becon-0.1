# EMF 		From...Import
from handle_Logging		 	import EMF_Logging_Handle
from handle_DataSeries	 	import EMF_DataSeries_Handle
from handle_WordSeries 		import EMF_WordSeries_Handle
from lib_EMF		 		import TEMP_MODE
from util_CreateDB	 		import create_DB
from util_Logging	 		import init_logging
# EMF 		Import...As
# System 	Import...As
import logging 	as log

class EMF_Testing_Handle:
	def __init__(self, mode=TEMP_MODE):
		(self.logLoc, self.deleteLog) = init_logging(mode=mode)
		self.hndl_DB = create_DB(mode=mode)
		self.hndl_Log = EMF_Logging_Handle(mode=mode)
		self.wordHandles = {}

	def __del__(self):
		del self.hndl_DB
		del self.hndl_Log

	def insert_test_data(self, dates, dataSet, dataTickers):
		dataHandle = EMF_DataSeries_Handle(self.hndl_DB)
		for (idx, ticker) in enumerate(dataTickers):
			try:
				values = dataSet[:,idx]
			except IndexError:
				values = dataSet
			dataHandle.set_data_series(name=ticker, ticker=ticker, insertIfNot=True)
			dataHandle.write_to_DB(dates, values)
			dataHandle.unset_data_series()

	def create_word_from_data(self, dataTicker, transformationPattern):
		wordHandle = EMF_WordSeries_Handle(self.hndl_DB, dataTicker, transformationPattern)
		self.wordHandles[str(wordHandle)] = wordHandle
		return str(wordHandle)

	def retrieve_word(self, wordName):
		return self.wordHandles[wordName]