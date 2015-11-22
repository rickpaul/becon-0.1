import sqlite3 as sq
from os import remove

import EMF_DatabaseCreator
import EMF_DatabaseCreator_util
import EMF_DatabaseInstructions
from EMF_Database_lib import DBRepository

DBFilePath = DBRepository + 'delete_me.db'
conn = None

def createTestDB():
	'''
	TODOS:
	Refactor this into own testing library
	'''
	tableCreationInstructions = EMF_DatabaseCreator.fullTableCreationInstructions
	EMF_DatabaseCreator_util.doOneTimeDBCreation(DBFilePath, tableCreationInstructions, force=True)

def checkDBCreatorUtil(conn, cursor):
	assert EMF_DatabaseCreator_util.checkTableExists(conn, cursor, 'T_DATA_SERIES')


def checkDBCreatorInsertion(conn, cursor):
	ID = EMF_DatabaseInstructions.retrieve_DataSeriesID(conn, cursor, dataName='test', dataTicker='test', insertIfNot=False)
	assert ID == None
	ID = EMF_DatabaseInstructions.retrieve_DataSeriesID(conn, cursor, dataName='test', dataTicker='test', insertIfNot=True)
	assert ID == 1

def checkDBMetadataFinder(conn, cursor):
	data = EMF_DatabaseInstructions.retrieve_DataSeriesMetaData(conn, cursor, 'txt_data_name', 1)
	assert data == 'test'
	data = EMF_DatabaseInstructions.retrieve_DataSeriesMetaData(conn, cursor, 'dt_last_updated_history', 1)
	assert data == None

def checkDBMetadataUpdater(conn, cursor):
	EMF_DatabaseInstructions.update_DataSeriesMetaData(conn, cursor, 'dt_last_updated_history', 90876, 1)
	data = EMF_DatabaseInstructions.retrieve_DataSeriesMetaData(conn, cursor, 'dt_last_updated_history', 1)
	assert data == 90876

def checkDBHistoryInsertion(conn, cursor):
	seriesID = 1
	date=0
	value=201
	EMF_DatabaseInstructions.insertDataPoint_DataHistoryTable(conn, cursor, seriesID, date, value)
	EMF_DatabaseInstructions.insertDataPoint_DataHistoryTable(conn, cursor, seriesID, date+1, value+1)
	assert [(date, value),(date+1, value+1)] == EMF_DatabaseInstructions.getCompleteDataHistory_DataHistoryTable(conn, cursor, seriesID)

def cleanupDB():
	if conn is not None:
		conn.close()
	remove(DBFilePath)


def main():
	try:
		createTestDB()
		conn = sq.connect(DBFilePath)
		cursor = conn.cursor()
		checkDBCreatorUtil(conn, cursor)
		checkDBCreatorInsertion(conn, cursor)
		checkDBMetadataFinder(conn, cursor)
		checkDBMetadataUpdater(conn, cursor)
		checkDBHistoryInsertion(conn, cursor)

	except Exception, e:
		raise
	else:
		pass
	finally:
		cleanupDB()
	

if __name__ == '__main__':
	main()