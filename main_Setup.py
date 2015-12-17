import logging as log
# from sys 			import argv
from os.path 		import exists
from os 			import makedirs

from lib_DB 		import DBRepository
from lib_Logging 	import LogRepository
from lib_QuandlAPI 	import CSVRepository

import util_Logging as log_util

AllDirectories = [DBRepository, LogRepository, CSVRepository]

def main():
	log_util.initializeLog()
	for directory in AllDirectories:
		if not exists(directory):
			log.info('Creating Directory at %s', directory)
			makedirs(directory)

if __name__ == '__main__':
	main()
