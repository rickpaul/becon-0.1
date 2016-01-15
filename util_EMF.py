# EMF 		From...Import
from 	lib_EMF		 		import 	TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
# EMF 		Import...As
import 	lib_DB
import 	lib_Logging
import 	lib_QuandlAPI


######################## DIRECTORY CODE
def get_EMF_settings(mode=TEMP_MODE):
	if mode==TEMP_MODE:
		return {
			'dbLoc':		lib_DB.TempDBFilePath,
			'overwriteDB':	True,
			'deleteDB':		True,
			'logLoc':		lib_Logging.TempLogFilePath,
			'recordLog':	False,
			'recordLevel':	log.INFO,
			'deleteLog':	None,
			'logAppend':	True,
			'QuandlCSVLoc': lib_QuandlAPI.TempQuandlCSV,
		}
	elif mode==TEST_MODE:
		return {
			'dbLoc':		lib_DB.TestDBFilePath,
			'overwriteDB':	True,
			'deleteDB':		False,
			'logLoc':		lib_Logging.TestLogFilePath,
			'recordLog':	False,
			'recordLevel':	log.DEBUG,
			'deleteLog':	None,
			'logAppend':	False,
			'QuandlCSVLoc': lib_QuandlAPI.TestQuandlCSV,
		}
	elif mode==QA_MODE:
		return {
			'dbLoc':		lib_DB.QADBFilePath,
			'overwriteDB':	False,
			'deleteDB':		False,
			'logLoc':		lib_Logging.QALogFilePath,
			'recordLog':	True,
			'recordLevel':	log.INFO,
			'deleteLog':	False,
			'logAppend':	True,
			'QuandlCSVLoc': lib_QuandlAPI.QAQuandlCSV,
		}
	elif mode==PROD_MODE:
		return {
			'dbLoc':		lib_DB.ProdDBFilePath,
			'overwriteDB':	False,
			'deleteDB':		False,
			'logLoc':		lib_Logging.ProdLogFilePath,
			'recordLog':	True,
			'recordLevel':	log.WARNING,
			'deleteLog':	False,
			'logAppend':	True,
			'QuandlCSVLoc': lib_QuandlAPI.ProdQuandlCSV,
		}
	else:
		raise NameError('EMF Run Mode not recognized')
