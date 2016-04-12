# TODO:
# 	Move the DB connections out of this. We don't need to keep it here.

# EMF 		From...Import
from 	handle_DB_SQLite 	import EMF_SQLite_Handle
from 	handle_DB_mySQL 	import EMF_MySQL_Handle
from 	lib_DB		 		import SQLITE_MODE, MYSQL_MODE
from 	lib_EMF		 		import TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
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
			# MySQL DB
			'dbName':		lib_DB.TempDB_MySQL,
			# Log
			'logLoc':		lib_Log.TempLogFilePath,
			'recordLog':	False,
			'recordLevel':	log.DEBUG,
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
			# MySQL DB
			'dbName':		lib_DB.TestDB_MySQL,
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
			# MySQL DB
			'dbName':		lib_DB.QADB_MySQL,
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
			# MySQL DB
			'dbName':		lib_DB.ProdDB_MySQL,
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


def get_DB_Handle(EMF_mode, DB_mode, allow_delete=True):
	settings = get_EMF_settings(EMF_mode)
	if DB_mode==SQLITE_MODE:
		dbLoc = settings['dbLoc']
		deleteDB = settings['deleteDB'] and allow_delete
		return EMF_SQLite_Handle(dbLoc, deleteDB=deleteDB)
	elif DB_mode==MYSQL_MODE:
		dbName = settings['dbName']
		deleteDB = settings['deleteDB']
		return EMF_MySQL_Handle(dbName, deleteDB=deleteDB)
	else:
		raise NameError('EMF DB Mode not recognized')
