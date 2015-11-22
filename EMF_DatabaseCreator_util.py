import os
import sqlite3 	as sq
import logging 	as log
from sys import argv
import EMF_Database_util as EMF_DB_Util

def checkTableExists(conn, cursor, tableName):
	'''
	Checks for a table within a database

	PARAMETERS:
	conn <sqlite3 connection> 
	cursor <sqlite3 connection> 
	tableName <string> a table name

	RETURNS:
	<bool> whether a table exists
	'''	
	statement = 'select name from sqlite_master where type="table" and name = "{0}";'.format(tableName)
	(success, name) = EMF_DB_Util.retrieveDBStatement(cursor, statement, expectedColumnCount=1, expectedCount=1)
	return success and (name == tableName) #Second part not strictly necessary, as select will fail if not found

def dropTable(conn, cursor, tableName):
	'''
	Drops a table from a database

	PARAMETERS:
	conn <sqlite3 connection> 
	cursor <sqlite3 connection> 
	tableName <string> a table name

	RETURNS:
	(success, error) <(bool, string)> tuple of whether successful and what error if not
	'''
	statement = 'drop table if exists {0};'.format(tableName)
	return EMF_DB_Util.commitDBStatement(conn, cursor, statement)


def checkIfDBTablesExist(DBFilePath, tableNames):
	'''
	Checks if a full DB exists with a list of expected tables

	PARAMETERS:
	DBFilePath <string> full local path to a Database
	tableNames <list> list of table names

	RETURNS:
	Whether all tables exist in the database

	TODO:
	Deprecated? Where is this used? Delete this.
	'''
	# Check if DB File Exists
	if not os.path.isfile(DBFilePath):
		return False

	conn = sq.connect(DBFilePath)
	cursor = conn.cursor()
	# Check for Existence of Individual Tables
	try:
		for tableName in tableNames:
			exists = checkTableExists(conn, cursor, tableName)
			if not exists:
				log.warning("%s doesn't exist.", tableName)
				return False
			log.debug("%s exists as expected.", tableName)
		log.info("DB exists with appropriate tables.")
		return True
	except:
		raise
	finally:
		conn.close()


def doOneTimeDBCreation(DBFilePath, tableCreationInstructions, force=False):
	'''
	Given a DB path and table creation instructions, creates a DB and its tables

	PARAMETERS:
	DBFilePath <string> full local path to a Database
	tableCreationInstructions <dictionary> key={table name} and value={SQL creation instruction}
	force <bool> should we delete/overwrite existing tables?
	
	RETURNS:
	Nothing
	'''
	# Find Database Directory
	directory = os.path.dirname(DBFilePath)
	# Create Directory if Necessary
	if not os.path.exists(directory):
		print 'Creating OS Directory'
		os.makedirs(directory)
	# Connect to Database
	conn = sq.connect(DBFilePath)
	cursor = conn.cursor()
	try:
		for (tableName, instruction) in tableCreationInstructions.iteritems():
			if checkTableExists(conn, cursor, tableName):
				if force:
					log.warning("Dropping Table %s for overwrite.", tableName)
					dropTable(conn, cursor, tableName)
				else:
					log.error('Table %s already exists', tableName)
					raise Exception
			log.info("Creating Table %s in %s.", tableName, DBFilePath)
			(success, error) = EMF_DB_Util.commitDBStatement(conn, cursor, instruction)
	except:
		log.error("Creating %s Failed!", DBFilePath)
		raise
	finally:
		conn.close()
