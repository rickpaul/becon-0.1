import sqlite3 	as sq
import numpy 	as np
import logging 	as log
from os import remove
from os.path import isfile

import EMF_DatabaseCreator_util as EM_DBMake

from EMF_Logging_util import initializeLog
from EMF_Database_lib import testDB
from EMF_Database_lib import DBRepository
from EMF_DataSeriesHandle import EMF_DataSeries_Handle
from EMF_WordSeriesHandle import EMF_WordSeries_Handle
from EMF_DatabaseCreator import fullTableCreationInstructions

deleteDB = True
DBFilePath = DBRepository + 'delete_me.db' if deleteDB else testDB
db_connection = None

def createTestData_2D_Circle(n=300):
	dt = np.reshape(np.arange(n), (n,1))
	x = np.random.random_sample((n,2))*3
	y = np.reshape(
			5.5-((x[:,0]-1.5)**2 + (x[:,1]-1.5)**2),
		(n,1))
	dataSet = np.hstack((dt,x,y))
	return dataSet

def insertTestData_2D_Circle(db_connection, db_cursor):
	# Create Data Set
	dataSet = createTestData_2D_Circle()

	# Add Data Set to DB
	dataHandle = EMF_DataSeries_Handle(db_connection, db_cursor)

	dataTickers =  ['x1', 'x2', 'y']
	for (idx, ticker) in enumerate(dataTickers):
		name = ticker
		dataHandle.setDataSeries(name=name, ticker=ticker, insertIfNot=True)
		dataHandle.insertDataHistory(dataSet[:,0], dataSet[:,idx+1])
		dataHandle.unsetDataSeries()

def createWords(db_connection, db_cursor):
	wordHandle = EMF_WordSeries_Handle(db_connection, db_cursor)
	wordHandle.setDataSeries('y')
	wordHandle.setTransformation_FromTemplate('Stratification')

def performInitialSetup(DBFilePath, logFilePath=None, recordLog=False, quietShell=False):
	# Initialize Log
	if quietShell and not recordLog:
		recordLevel=log.INFO
	else:
		recordLevel=None

	initializeLog(recordLog=recordLog, logFilePath=logFilePath, recordLevel=recordLevel)
	log.info('Log Initialized.')

	# Create Database
	log.info('Connecting to Database: \n%s', DBFilePath)		
	if not isfile(DBFilePath):
		log.info('Database not found. Creating new database...')
		EM_DBMake.doOneTimeDBCreation(DBFilePath, fullTableCreationInstructions)

	# Store Database Connection
	db_connection = sq.connect(DBFilePath)
	db_cursor = db_connection.cursor()
	log.info('Database opened successfully')
	return (db_cursor, db_connection)


def finalize(db_connection):
	if db_connection is not None:
		db_connection.close()
		log.info('Database connection closed successfully')
	if deleteDB:
		remove(DBFilePath)
		log.info('Database deleted successfully')

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