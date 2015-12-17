# EMF 		From...Import
from handle_DataSeries	 	import EMF_DataSeries_Handle
from handle_WordSeries 		import EMF_WordSeries_Handle
from lib_EMF		 		import TEMP_MODE
from util_CreateDB	 		import create_DB
# EMF 		Import...As
# System 	Import...As
import logging 	as log
# System 	From...Import
from os import remove

class EMF_Testing_Handle:
	def __init__(self, mode=TEMP_MODE):
		# self.logLoc = do_DB_Creation(mode=mode)
		self.hndl_DB = create_DB(mode=mode)
		self.wordHandles = {}

	def __del__(self):
		del self.hndl_DB
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

	# def __setup(self, quietShell=False):
	# 	raise NotImplementedError #DELETE THIS! DEPRECATED NOW
	# 	# Initialize Log
	# 	if quietShell:
	# 		recordLevel=log.INFO
	# 	else:
	# 		recordLevel=None

	# 	initializeLog(recordLog=True, logFilePath=temporaryLog, recordLevel=recordLevel)
	# 	log.info('Log Initialized at {}.').format(temporaryLog))


	# def runTest(testMethod, verbose=True):
	# 	raise NotImplementedError #DELETE THIS! DEPRECATED NOW
	# 	try:
	# 		__setup(quietShell=(not verbose))
	# 	except Exception as e:
	# 		print('ERROR!')
	# 		print(e)
	# 	finally:
	# 		__finalize()