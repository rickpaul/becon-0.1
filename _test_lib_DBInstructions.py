import sqlite3 as sq
from os import remove

from main_CreateDB import fullTableCreationInstructions
import util_CreateDB
import lib_DBInstructions
from lib_DB import DBRepository

DBFilePath = DBRepository + 'delete_me.db'
conn = None

def createTestDB():
	'''
	TODOS:
	Refactor this into own testing library
	'''
	tableCreationInstructions = fullTableCreationInstructions
	util_CreateDB.doOneTimeDBCreation(DBFilePath, tableCreationInstructions, force=True)

def checkDBCreatorUtil(conn, cursor):
	assert util_CreateDB.checkTableExists(conn, cursor, 'T_DATA_SERIES')


def checkDBCreatorInsertion(conn, cursor):
	ID = lib_DBInstructions.retrieve_DataSeriesID(conn, cursor, dataName='test', dataTicker='test', insertIfNot=False)
	assert ID == None
	ID = lib_DBInstructions.retrieve_DataSeriesID(conn, cursor, dataName='test', dataTicker='test', insertIfNot=True)
	assert ID == 1

def checkDBMetadataFinder(conn, cursor):
	data = lib_DBInstructions.retrieve_DataSeriesMetaData(conn, cursor, 'txt_data_name', 1)
	assert data == 'test'
	data = lib_DBInstructions.retrieve_DataSeriesMetaData(conn, cursor, 'dt_last_updated_history', 1)
	assert data == None

def checkDBMetadataUpdater(conn, cursor):
	lib_DBInstructions.update_DataSeriesMetaData(conn, cursor, 'dt_last_updated_history', 90876, 1)
	data = lib_DBInstructions.retrieve_DataSeriesMetaData(conn, cursor, 'dt_last_updated_history', 1)
	assert data == 90876

def checkDBHistoryInsertion(conn, cursor):
	seriesID = 1
	date=0
	value=201
	lib_DBInstructions.insertDataPoint_DataHistoryTable(conn, cursor, seriesID, date, value)
	lib_DBInstructions.insertDataPoint_DataHistoryTable(conn, cursor, seriesID, date+1, value+1)
	assert [(date, value),(date+1, value+1)] == lib_DBInstructions.getCompleteDataHistory_DataHistoryTable(conn, cursor, seriesID)

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