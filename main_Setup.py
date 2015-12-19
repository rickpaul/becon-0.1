# EMF 		From...Import
from lib_DB 		import DBRepository
from lib_Logging 	import LogRepository
from lib_QuandlAPI 	import CSVRepository
from lib_JSON		import JSONRepository
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
	JSONRepository
]

def main():
	log_util.initializeLog()
	for directory in AllDirectories:
		if not exists(directory):
			log.info('Creating Directory at %s', directory)
			makedirs(directory)

if __name__ == '__main__':
	main()
