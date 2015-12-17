# TODO: 
#	Implement Options, Log channeling


# EMF 		From...Import
from 	lib_EMF		 		import TEMP_MODE
from 	util_EMF			import get_EMF_settings
# EMF 		Import...As
import 	lib_Logging 		as log_lib
# System 	Import...As
import 	logging 			as log
# System 	From...Import
from 	os.path 	import exists, dirname
from 	os 			import makedirs

def __create_log_directory(logFilePath):
	# Find Database Directory
	directory = dirname(logFilePath)
	# Create Directory if Necessary
	if not exists(directory):
		log.info('Creating OS Directory for DB at {0}'.format(directory))
		makedirs(directory)

def __initialize_log(logFilePath=None, recordLevel=None, recordLog=True, clearRecorded=True):
	if recordLog:
		fileMode = 'wb' if clearRecorded else 'ab'
		recordLevel = log.INFO if recordLevel is None else recordLevel
		logFilePath = log_lib.TempLogFilePath if logFilePath is None else logFilePath
		log.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', 
						datefmt='%m/%d/%Y %I:%M:%S %p',
						filename=logFilePath,
						filemode=fileMode,
						level=recordLevel)	
	else:
		recordLevel = log.DEBUG if recordLevel is None else recordLevel
		log.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', 
						datefmt='%I:%M:%S %p',
						level=recordLevel)			

def init_logging(mode=TEMP_MODE):
	settings = get_EMF_settings(mode)
	logLocation = settings['logLoc']
	recordLog = settings['recordLog']
	recordLevel = settings['recordLevel']
	clearRecorded = not(settings['logAppend'])
	deleteLog = recordLog and settings['deleteLog']
	__initialize_log(	logFilePath=logLocation, 
						recordLevel=recordLevel, 
						recordLog=recordLog, 
						clearRecorded=clearRecorded)
	return (logLocation, deleteLog)