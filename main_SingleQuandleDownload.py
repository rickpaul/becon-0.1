# TODO:
# 	Make Interactive/Finish

# EMF 		From...Import
from 	handle_QuandlAPI	import EMF_QuandlAPI_Handle
from 	lib_EMF				import TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
from 	util_DB				import connect_to_DB
# System 	From...Import
from 	sys 				import argv
import	logging 			as 	log


if __name__ == '__main__':
	raise NotImplementedError
	# Read Arguments
	args = argv[1:]
	(Q_DATABASE_CODE, Q_DATASET_CODE) = (args[0], args[1])
	if len(args) == 2:
		pass
	elif len(args) == 3:
		(Q_DATABASE_CODE, Q_DATASET_CODE, Q_COLUMN_NUM) = (args[0], args[1], args[2])
	else:
		exit(1)

	try:
		hndl_Qndl = EMF_QuandlAPI_Handle(Q_DATABASE_CODE, Q_DATASET_CODE)
		hndl_Qndl.get_data() #hndl_Qndl Now has dates, values, and metadata saved
		hndl_Data = EMF_DataSeries_Handle(self._hndl_DB, name=db_name, ticker=db_ticker, insertIfNot=True)

	except Exception, e:
		log.error('QUANDL_SINGLE: Unspecified Error.')
		log.error('QUANDL_SINGLE: ' + e)
		exit(1)
	exit(0)