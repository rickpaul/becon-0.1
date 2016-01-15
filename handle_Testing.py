# EMF 		From...Import
from handle_DataSeries	 	import EMF_DataSeries_Handle
from handle_Logging		 	import EMF_Logging_Handle
from handle_Transformation	import EMF_Transformation_Handle
from handle_WordSeries		import EMF_WordSeries_Handle
from lib_EMF		 		import TEMP_MODE, TEST_MODE
from util_CreateDB	 		import create_or_connect_DB
# EMF 		Import...As
# System 	Import...As
import logging 	as log

class EMF_Testing_Handle:
	def __init__(self, mode=TEMP_MODE):
		self.hndl_Log = EMF_Logging_Handle(mode=mode)
		if mode != TEMP_MODE and mode != TEST_MODE:
			log.ERROR('Attempting a test on a non-test Database')
			return
		self.hndl_DB = create_or_connect_DB(mode=mode)
		self.wordHandles = {}

	def __del__(self):
		del self.hndl_DB
		del self.hndl_Log

	def insert_test_data(self, dates, values, tickers, periodicity=1, categorical=None):
		for (i, t) in enumerate(tickers):
			try:
				values = values[:,i]
			except IndexError:
				values = values
			hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, name=t, ticker=t, insertIfNot=True)
			if categorical is not None:
				hndl_Data.set_categorical(categorical[i])	
			hndl_Data.set_periodicity(periodicity)
			hndl_Data.save_series_db(dates, values)

	def retrieve_test_word(self, ticker, transPattern):
		'''
		This function doesn't really need to exist but it makes things easier
		'''
		hndl_Data = self.retrieve_test_data(ticker)
		hndl_Trns = EMF_Transformation_Handle(transPattern)
		return EMF_WordSeries_Handle(self.hndl_DB, hndl_Data, hndl_Trns)

	def retrieve_test_data(self, ticker):
		'''
		This function doesn't really need to exist but it makes things easier
		'''
		hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, ticker=ticker)
		return hndl_Data


