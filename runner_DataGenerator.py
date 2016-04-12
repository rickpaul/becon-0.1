#TODO:
#	This is kind of a stand-in until we get the transformations fully developed.
#	Change this into a util/main
# 	Add categories to US_TimeSince/UntilRecession
# Move out Main
# connect_to_db? -> from 	util_EMF import get_DB_Handle

# EMF 		From...Import
from 	handle_EMF					import EMF_Settings_Handle
from 	handle_Logging 			import EMF_Logging_Handle
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_WordSeries 		import EMF_WordSeries_Handle
# from 	lib_DB					import SQLITE_MODE, MYSQL_MODE
# from 	lib_EMF					import TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
from 	util_Transformation 	import transform_TimeSinceValue, transform_TimeToValue
from 	util_Transformation 	import TIME_SINCE_VALUE, TIME_TO_VALUE, DATA_KEY
from 	util_DB 	 			import connect_to_DB

class EMF_DataGenerator_Runner:
	def __init__(self, hndl_DB):
		self.hndl_DB = hndl_DB

	def insert_time_to_peak(self):
		raise NotImplementedError

	def insert_time_to_recession(self):
		# Get Data Read
		hndl_Data_Read = EMF_DataSeries_Handle(self.hndl_DB, ticker='US_Rec_Ind')
		hndl_Data_Read.save_series_local()
		# Insert Time To
		hndl_Data_Wrte = EMF_DataSeries_Handle(	self.hndl_DB, 
												name='Months to Next Recession', 
												ticker='US_TimeUntilRec',
												insertIfNot=True)
		data = hndl_Data_Read.get_series_values()
		dates = hndl_Data_Read.get_series_dates()
		trns_Data = transform_TimeToValue(data, {TIME_TO_VALUE: 1})[DATA_KEY]
		count = self.find_time_to_recession_limits(trns_Data)
		trns_Data = trns_Data[:-count]
		trns_Dates = dates[:-count]
		hndl_Data_Wrte.save_series_db(trns_Dates, trns_Data)
		hndl_Data_Wrte.periodicity = hndl_Data_Read.periodicity
		# Insert Time Since
		hndl_Data_Wrte = EMF_DataSeries_Handle(	self.hndl_DB, 
												name='Months since Last Recession', 
												ticker='US_TimeSinceRec',
												insertIfNot=True)
		
		trns_Data = transform_TimeSinceValue(data, {TIME_SINCE_VALUE: 1})[DATA_KEY]
		count = self.find_time_since_recession_limits(trns_Data)
		trns_Data = trns_Data[count:]
		trns_Dates = dates[count:]
		hndl_Data_Wrte.save_series_db(trns_Dates, trns_Data)		
		hndl_Data_Wrte.periodicity = hndl_Data_Read.periodicity

	def find_time_since_recession_limits(self, data):
		count = 0
		for i in data:
			if i != -1:
				return count
			count += 1

	def find_time_to_recession_limits(self, data):
		count = 0
		for i in reversed(data):
			if i != -1:
				return count
			count += 1

######################## CURRENT RUN PARAMS
settings = EMF_Settings_Handle()

def main():
	DB_MODE = settings.DB_MODE
	EMF_MODE = settings.EMF_MODE
	hndl_Log = EMF_Logging_Handle(mode=EMF_MODE)
	hndl_DB = get_DB_Handle(EMF_mode=EMF_MODE, DB_mode=DB_MODE)
	dataGen = EMF_DataGenerator_Runner(hndl_DB)
	dataGen.insert_time_to_recession()

if __name__ == '__main__':
	main()