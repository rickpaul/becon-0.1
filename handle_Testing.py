# EMF 		From...Import
from handle_DataSeries	 	import EMF_DataSeries_Handle
from handle_Logging		 	import EMF_Logging_Handle
from handle_Transformation	import EMF_Transformation_Handle
from handle_WordSeries		import EMF_WordSeries_Handle
from lib_EMF		 		import TEMP_MODE
from util_CreateDB	 		import create_DB
# EMF 		Import...As
# System 	Import...As
import logging 	as log

class EMF_Testing_Handle:
	def __init__(self, mode=TEMP_MODE):
		self.hndl_DB = create_DB(mode=mode)
		self.hndl_Log = EMF_Logging_Handle(mode=mode)
		self.wordHandles = {}

	def __del__(self):
		del self.hndl_DB
		del self.hndl_Log

	def insert_test_data(self, dates, dataSet, dataTickers, periodicity=1, categorical=None):
		hndl_Data = EMF_DataSeries_Handle(self.hndl_DB)
		for (idx, ticker) in enumerate(dataTickers):
			try:
				values = dataSet[:,idx]
			except IndexError:
				values = dataSet
			hndl_Data.set_data_series(name=ticker, ticker=ticker, insertIfNot=True)
			if categorical is not None:
				hndl_Data.set_categorical(categorical)	
			hndl_Data.set_periodicity(periodicity)
			hndl_Data.write_to_DB(dates, values)
			hndl_Data.unset_data_series()

	def retrieve_test_word(self, dataTicker, transPattern):
		hndl_Data = EMF_DataSeries_Handle(self.hndl_DB)
		hndl_Data.set_data_series(ticker=dataTicker)
		hndl_Trns = EMF_Transformation_Handle(transPattern)
		return EMF_WordSeries_Handle(self.hndl_DB, hndl_Data, hndl_Trns)		