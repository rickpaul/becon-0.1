import logging as log

import EMF_Logging_lib as EMF_Log_Lib

# TODO: Implement Options, Log channeling
def initializeLog(recordLog=False, clearRecorded=True, recordLevel=None, logFilePath=None):
	if recordLog:
		fileMode = 'wb' if clearRecorded else 'ab'
		recordLevel = log.INFO if recordLevel is None else recordLevel
		logFilePath = EMF_Log_Lib.defaultLog if logFilePath is None else logFilePath
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
