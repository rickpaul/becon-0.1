# EMF 		From...Import
from 	handle_QuandlAPI	import EMF_QuandlAPI_Handle

# System 	From...Import
from 	sys 				import argv
import	logging 			as 	log

if __name__ == '__main__':
	# Read Arguments
	args = argv[1:]
	(Q_DATABASE_CODE, Q_DATASET_CODE) = (args[0], args[1])
	if len(args) == 2:
	elif len(args) == 3:
		(Q_DATABASE_CODE, Q_DATASET_CODE, Q_COLUMN_NUM) = (args[0], args[1], args[2])
	else:
		exit(1)

	try:
		hndl_Qndl = EMF_QuandlAPI_Handle(Q_DATABASE_CODE, Q_DATASET_CODE)
		hndl_Qndl.get_data() #hndl_Qndl Now has dates, values, and metadata saved
		
	except Exception, e:
		log.error('QUANDL_SINGLE: Unspecified Error.')
		log.error('QUANDL_SINGLE: ' + e)
		exit(1)
	exit(0)