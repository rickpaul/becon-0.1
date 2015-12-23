# TODOS:
#	Fold into testing framework? 
#		The testing framework relies on the data handle. Maybe better to keep separate
#	THIS IS AN INCOMPLETE TEST! JUST A NUB.
#	Make cleaner

# EMF 		From...Import
from lib_EMF		 	import TEMP_MODE
from util_CreateDB	 	import create_DB
from lib_DataSeries	 	import DATE_COL, VALUE_COL
from handle_DataSeries 	import EMF_DataSeries_Handle
# EMF 		Import...As
# System 	Import...As
# System 	From...Import

import numpy as np

def testDataSeriesHandle(hndl_DB):
	dates = np.reshape(np.arange(200),(200,))
	data = np.random.randint(100,size=(200,))/2.0
	dataHandle = EMF_DataSeries_Handle(hndl_DB)
	name = 'test1'
	ticker = 'test1'
	dataHandle.set_data_series(name=name, ticker=ticker)	
	assert dataHandle.seriesName == name
	assert dataHandle.seriesTicker == ticker
	dataHandle.write_to_DB(dates, data)
	dataSeries = dataHandle.get_data_history()
	assert np.all(dataSeries[DATE_COL] == dates)
	assert np.all(dataSeries[VALUE_COL] == data)
	assert dataHandle.get_earliest_date()==0
	assert dataHandle.get_latest_date()==199
	dataHandle.unset_data_series()	
	assert dataHandle.seriesName == None
	assert dataHandle.seriesTicker == None

def testWriteToJSON(hndl_DB):
	dataHandle = EMF_DataSeries_Handle(hndl_DB)
	name = 'test1'
	ticker = 'test1'
	dataHandle.set_data_series(name=name, ticker=ticker)	
	dataHandle.write_to_JSON()

def main():
	try:
		np.random.seed(10)
		hndl_DB = create_DB(mode=TEMP_MODE)
		testDataSeriesHandle(hndl_DB)
		testWriteToJSON(hndl_DB)
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

if __name__ == '__main__':
	main()