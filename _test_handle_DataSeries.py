# TODOS:
#	Fold into testing framework? 
#		The testing framework relies on the data handle. Maybe better to keep separate
#	THIS IS AN INCOMPLETE TEST! JUST A NUB.
#	Make cleaner

# EMF 		From...Import
from lib_EMF		 	import TEMP_MODE
from util_CreateDB	 	import create_or_connect_to_DB
from lib_DataSeries	 	import DATE_COL, VALUE_COL
from handle_DataSeries 	import EMF_DataSeries_Handle
# EMF 		Import...As
# System 	Import...As
# System 	From...Import

import numpy as np

def testDataSeriesHandle(hndl_DB):
	dates = np.reshape(np.arange(200),(200,))
	data = np.random.randint(100,size=(200,))/2.0
	name = 'test1'
	ticker = 'test1'
	dataHandle = EMF_DataSeries_Handle(hndl_DB, name=name, ticker=ticker, insertIfNot=True)
	dataHandle.save_series_db(dates, data)
	assert np.all(dataHandle.get_series_dates() == dates)
	assert np.all(dataHandle.get_series_values() == data)
	assert dataHandle.min_date==0
	assert dataHandle.max_date==199
	assert dataHandle.name == name
	assert dataHandle.ticker == ticker
	
# def testWriteToJSON(hndl_DB):
# 	name = 'test1'
# 	ticker = 'test1'
# 	dataHandle = EMF_DataSeries_Handle(hndl_DB, name=name, ticker=ticker, insertIfNot=True)
# 	dataHandle.write_to_JSON()

def main():
	try:
		np.random.seed(10)
		hndl_DB = create_or_connect_to_DB(mode=TEMP_MODE)
		testDataSeriesHandle(hndl_DB)
		# testWriteToJSON(hndl_DB)
	except Exception, e:
		raise
	else:
		pass
	finally:
		pass

if __name__ == '__main__':
	main()