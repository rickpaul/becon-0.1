# EMF 		From...Import
from 	lib_EMF		 		import 	TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
# EMF 		Import...As
import 	lib_DB
import 	lib_Logging 		as lib_Log
import 	lib_QuandlAPI
# System 	Import...As
import 	logging as log

######################## DIRECTORY CODE
def get_EMF_settings(mode=TEMP_MODE):
	if mode==TEMP_MODE:
		return {
			# SQLite DB
			'dbLoc':		lib_DB.TempDB_SQLite,
			'overwriteDB':	True,
			'deleteDB':		True,
			# Log
			'logLoc':		lib_Log.TempLogFilePath,
			'recordLog':	False,
			'recordLevel':	log.INFO,
			'deleteLog':	None,
			'logAppend':	True,
			# CSV
			'QuandlCSVLoc': lib_QuandlAPI.TempQuandlCSV,
		}
	elif mode==TEST_MODE:
		return {
			# SQLite DB
			'dbLoc':		lib_DB.TestDB_SQLite,
			'overwriteDB':	True,
			'deleteDB':		False,
			# Log
			'logLoc':		lib_Log.TestLogFilePath,
			'recordLog':	False,
			'recordLevel':	log.DEBUG,
			'deleteLog':	None,
			'logAppend':	False,
			# CSV
			'QuandlCSVLoc': lib_QuandlAPI.TestQuandlCSV,
		}
	elif mode==QA_MODE:
		return {
			# SQLite DB
			'dbLoc':		lib_DB.QADB_SQLite,
			'overwriteDB':	False,
			'deleteDB':		False,
			# Log
			'logLoc':		lib_Log.QALogFilePath,
			'recordLog':	True,
			'recordLevel':	log.INFO,
			'deleteLog':	False,
			'logAppend':	True,
			# CSV
			'QuandlCSVLoc': lib_QuandlAPI.QAQuandlCSV,
		}
	elif mode==PROD_MODE:
		return {
			# SQLite DB
			'dbLoc':		lib_DB.ProdDB_SQLite,
			'overwriteDB':	False,
			'deleteDB':		False,
			# Log
			'logLoc':		lib_Log.ProdLogFilePath,
			'recordLog':	True,
			'recordLevel':	log.WARNING,
			'deleteLog':	False,
			'logAppend':	True,
			# CSV
			'QuandlCSVLoc': lib_QuandlAPI.ProdQuandlCSV,
		}
	else:
		raise NameError('EMF Run Mode not recognized')
