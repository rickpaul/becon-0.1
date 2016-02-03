# TODO: 
#	Implement Log channeling


# EMF 		From...Import
from 	lib_EMF		import TEMP_MODE
from 	util_EMF	import get_EMF_settings
# EMF 		Import...As
import 	lib_Logging 		as log_lib
# System 	Import...As
import 	logging 	as log



class EMF_Logging_Handle:
	'''
	This class mostly exists to handle log deletion. 
	'''
	def __init__(self, mode=TEMP_MODE):
		# Get Settings
		settings = get_EMF_settings(mode)
		self._recordLog = settings['recordLog']
		self._deleteLog = self._recordLog and settings['deleteLog']
		self._recordLevel = settings['recordLevel']
		# Initialize Log
		if self._recordLog:
			self._logLocation = settings['logLoc']
			fileMode = 'wb' if not(settings['logAppend']) else 'ab'
			log.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', 
							datefmt='%m/%d/%Y %I:%M:%S %p',
							filename=self._logLocation,
							filemode=fileMode,
							level=self._recordLevel)	
		else:
			self._logLocation = None
			log.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', 
							datefmt='%I:%M:%S %p',
							level=self._recordLevel)
		# Declare Progress
		log.info('Log initialized.')
		if self._logLocation is not None:
			log.info('Log stored at %s.', self._logLocation)
			if self._deleteLog:
				log.info('Log will be deleted at completion.')

	def __del__(self):
		if self._recordLog:
			if self._deleteLog:
				log.warning('Log File {} deleted'.format(self._logLocation))
				remove(self.logLoc)
			else:
				log.info('Log File stored in {}'.format(self._logLocation))

	def logLoc_(self):
		return self._logLocation

	def logLevel_(self):
		return self._recordLevel