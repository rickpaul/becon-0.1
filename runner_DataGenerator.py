#TODO:
#	This is kind of a stand-in until we get the transformations fully developed.

# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_WordSeries 		import EMF_WordSeries_Handle
from 	util_Transformation 	import transform_TimeSinceValue, transform_TimeToValue
from 	lib_EMF					import TEMP_MODE, TEST_MODE
from 	util_CreateDB 			import connect_DB

class EMF_DataGenerator_Runner:
	def __init__(self, DBHandle):
		self.hndl_DB = DBHandle

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
		trns_Data = transform_TimeToValue(data, {'value': 1})
		count = self.find_time_to_recession_limits(trns_Data)
		trns_Data = trns_Data[:-count]
		trns_Dates = dates[:-count]
		hndl_Data_Wrte.save_series_to_db(trns_Dates, trns_Data)

		# Insert Time Since

		hndl_Data_Wrte = EMF_DataSeries_Handle(	self.hndl_DB, 
												name='Months since Last Recession', 
												ticker='US_TimeSinceRec',
												insertIfNot=True)
		
		trns_Data = transform_TimeSinceValue(data, {'value': 1})
		count = self.find_time_since_recession_limits(trns_Data)
		trns_Data = trns_Data[count:]
		trns_Dates = dates[count:]
		hndl_Data_Wrte.save_series_to_db(trns_Dates, trns_Data)		

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

def main():
	hndl_DB = connect_DB(mode=TEST_MODE)
	dataGen = EMF_DataGenerator_Runner(hndl_DB)
	dataGen.insert_time_to_recession()

if __name__ == '__main__':
	main()