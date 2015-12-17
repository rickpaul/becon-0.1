# TODO: 
#	Implement Options, Log channeling

import logging as log
import lib_Logging as log_lib

def initializeLog(logFilePath=None, recordLevel=None, recordLog=True, clearRecorded=True):
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
