# TODOS:
#	Fold into testing framework? The testing framework relies on the data handle. Maybe better to keep separate
#	THIS IS AN INCOMPLETE TEST! JUST A NUB.
#	Make cleaner
#	Test __get_from_DB/__send_to_DB

# EMF 		From...Import
from lib_EMF		 	import TEMP_MODE
from lib_DataSeries	 	import DATE_COL, VALUE_COL
from main_CreateDB	 	import do_DB_Creation
from handle_DataSeries 	import EMF_DataSeries_Handle
from handle_DB 			import EMF_Database_Handle
# EMF 		Import...As
# System 	Import...As
# System 	From...Import

import numpy as np

def testDataSeriesHandle(hndl_DB):
	np.random.seed(10)
	dates = np.reshape(np.arange(200),(200,))
	data = np.random.randint(100,size=(200,))/2.0
	dataHandle = EMF_DataSeries_Handle(hndl_DB)
	name = 'testSeries'
	ticker = 'test'
	dataHandle.set_data_series(name=name, ticker=ticker)	
	assert dataHandle.dataName == name
	assert dataHandle.dataTicker == ticker
	dataHandle.insert_data_history(dates, data)
	dataSeries = dataHandle.get_data_history()
	assert np.all(dataSeries[DATE_COL] == dates)
	assert np.all(dataSeries[VALUE_COL] == data)
	dataHandle.unset_data_series()	
	assert dataHandle.dataName == None
	assert dataHandle.dataTicker == None

def main():
	try:
		dbLoc = do_DB_Creation(mode=TEMP_MODE)
		hndl_DB = EMF_Database_Handle(dbLoc)
		testDataSeriesHandle(hndl_DB)
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

if __name__ == '__main__':
	main()