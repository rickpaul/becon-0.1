# EMF 		From...Import
from lib_DB 		import DBRepository
from lib_Logging 	import LogRepository
from lib_QuandlAPI 	import CSVRepository
from lib_JSON		import JSONRepository
from lib_Pickle		import PickleRepository
from lib_EMF		import TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
from util_CreateDB	import create_or_connect_to_DB
from util_EMF 		import get_EMF_settings
from handle_Logging	import EMF_Logging_Handle
# EMF 		Import...As
import util_Logging as log_util
# System 	Import...As
import logging as log
# System 	From...Import
from os.path 		import exists
from os 			import makedirs

AllDirectories = [
	DBRepository, 
	LogRepository, 
	CSVRepository, 
	JSONRepository,
	PickleRepository,
	WebRepository,
]

AllDatabases = [
	TEMP_MODE, 
	TEST_MODE, 
	QA_MODE, 
	PROD_MODE
]

def __createDatabases():
	for mode in AllDatabases:
		if not get_EMF_settings(mode=mode)['deleteDB']:
			create_or_connect_to_DB(mode=mode)

def __createDirectories():
	for directory in AllDirectories:
		if not exists(directory):
			log.info('Creating Directory at %s', directory)
			makedirs(directory)

def main():
	hndl_Log = EMF_Logging_Handle(mode=TEMP_MODE)
	__createDirectories()
	__createDatabases()

if __name__ == '__main__':
	main()
