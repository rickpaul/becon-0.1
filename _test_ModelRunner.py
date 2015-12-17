#TODO:
#	Change to use model_runner framework
#	Change to use test_handle framework

import sqlite3 	as sq
import numpy 	as np
import logging 	as log
from os import remove
from os.path import isfile


from util_Logging import initializeLog

from handle_DataSeries import EMF_DataSeries_Handle
from handle_WordSeries import EMF_WordSeries_Handle
from util_CreateDB import doOneTimeDBCreation
from main_CreateDB import fullTableCreationInstructions


def createWords(db_connection, db_cursor):
	wordHandle = EMF_WordSeries_Handle(db_connection, db_cursor)
	wordHandle.set_data_series('y')
	wordHandle.setTransformation_FromTemplate('Stratification')






def main():
	try:
		(db_cursor, db_connection) = performInitialSetup(DBFilePath, quietShell=1)
		insertTestData_2D_Circle(db_connection, db_cursor)
		createWords(db_connection, db_cursor)
	except Exception as e:
		print('ERROR!')
		print(e)
	finally:
		finalize(db_connection)

if __name__ == '__main__':
	main()