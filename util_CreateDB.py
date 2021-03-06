# EMF 		From...Import
from 	lib_EMF		import TEMP_MODE
from 	util_DB		import retrieveDBStatement, commitDBStatement
from 	util_EMF	import get_EMF_settings
from 	handle_DB	import EMF_Database_Handle
# EMF 		Import...As
import 	lib_CreateDB	as createDB_lib
# System 	Import...As
import 	logging 		as log
# System 	From...Import
from 	os.path 	import isfile

def __table_exists(conn, cursor, tableName):
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
	(success, name) = retrieveDBStatement(cursor, statement, expectedColumnCount=1, expectedCount=1)
	return success and (name == tableName) #Second part not strictly necessary, as select will fail if not found

def __drop_table(conn, cursor, tableName):
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
	return commitDBStatement(conn, cursor, statement)

def db_exists(DBFilePath):
	return isfile(DBFilePath)

def __create_table(conn, cursor, tableName, instruction, force=False):
	if __table_exists(conn, cursor, tableName):
		if force:
			log.warning('Dropping Table %s for overwrite.', tableName)
			__drop_table(conn, cursor, tableName)
		else:
			log.error('Table %s already exists', tableName)
			log.error('Databases already exist. If overwriting was your intent, use -mode-TEMP flag to force creation.')
			return 
	log.info("Table %s created.", tableName)
	(success, error) = commitDBStatement(conn, cursor, instruction)

def create_or_connect_to_DB(mode=TEMP_MODE, manualOverride=False):
	'''
	Given a DB path and table creation instructions, creates a DB and its tables

	PARAMETERS:
				mode | <string> | mode to get settings from util_EMF
				tableCreationInstructions | <dictionary> key={table name} and value={SQL creation instruction} | table creation instructions
				force | <bool> | should we delete/overwrite existing tables?
	
	RETURNS:
				DB Handle
	'''
	# Get Settings
	settings = get_EMF_settings(mode)
	force = settings['overwriteDB']
	dbLocation = settings['dbLoc']
	deleteDB  = settings['deleteDB']
	# Get Table Instruction
	if manualOverride:
		tableCreationInstructions = createDB_lib.create_instr_SQLite_Override
	else:
		tableCreationInstructions = createDB_lib.create_instr_SQLite
	# Create DB if necessary
	if db_exists(dbLocation):
		log.info('DB {0} found.'.format(dbLocation))
	else:
		log.info('DB {0} not found. Will be created.'.format(dbLocation))
	# Hook To DB
	hndl_DB = EMF_Database_Handle(dbLocation, deleteDB=deleteDB)
	# Create Tables
	try:
		log.info('Performing {0} table creation'.format('manual' if manualOverride else 'full'))
		for (tableName, instruction) in tableCreationInstructions.iteritems():
			__create_table(hndl_DB.conn, hndl_DB.cursor, tableName, instruction, force=force)
	except:
		log.error('Database Creation Failed.')
		raise
	return hndl_DB
