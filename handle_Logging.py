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
		self.__recordLog = settings['recordLog']
		self.__deleteLog = self.__recordLog and settings['deleteLog']
		self.__recordLevel = settings['recordLevel']
		# Initialize Log
		if self.__recordLog:
			self.__logLocation = settings['logLoc']
			fileMode = 'wb' if not(settings['logAppend']) else 'ab'
			log.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', 
							datefmt='%m/%d/%Y %I:%M:%S %p',
							filename=self.__logLocation,
							filemode=fileMode,
							level=self.__recordLevel)	
		else:
			self.__logLocation = None
			log.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', 
							datefmt='%I:%M:%S %p',
							level=self.__recordLevel)
		# Declare Progress
		log.info('Log initialized.')
		if self.__logLocation is not None:
			log.info('Log stored at %s.', self.__logLocation)
			if self.__deleteLog:
				log.info('Log will be deleted at completion.')

	def __del__(self):
		if self.__recordLog:
			if self.__deleteLog:
				log.warning('Log File {} deleted'.format(self.__logLocation))
				remove(self.logLoc)
			else:
				log.info('Log File stored in {}'.format(self.__logLocation))

	def logLoc_(self):
		return self.__logLocation

	def logLevel_(self):
		return self.__recordLevel