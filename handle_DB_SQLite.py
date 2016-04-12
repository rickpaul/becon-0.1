# TODO:
# 	Allow Manual Table Writing (Selective Overwrite of Tables)

# EMF 		From...Import
from 	handle_DB 			import EMF_Database_Handle
from 	lib_CreateDB		import create_instr_SQLite
from 	template_DB 		import EMF_Database_Template
from 	util_DB				import retrieveDBStatement, commitDBStatement
# EMF 		From...Import
# System 	Import...As
import 	sqlite3				as sq
import 	logging 			as log
# System 	From...Import
from 	os 					import remove
from 	os.path 			import isfile

class EMF_SQLite_Handle(EMF_Database_Handle, EMF_Database_Template):
	def __init__(self, dbLoc, deleteDB=False):
		'''
		CONSIDER:
					__conn and _cursor aren't passed by copy. Are they actually protected?
		'''
		self._dbLoc = dbLoc
		self._deleteDB = deleteDB
		self.connect_to_DB()

	def __del__(self):
		self._conn.close()
		log.info('DB_HANDLE: Database %s closed.', self._dbLoc)
		if self._deleteDB:
			remove(self._dbLoc)
			log.warning('DB_HANDLE: Database %s deleted.', self._dbLoc)

	def dbLoc():
		doc = 'The dbLoc property.'
		def fget(self):
			return self._dbLoc
		return locals()
	dbLoc = property(**dbLoc())

	def connect_to_DB(self):
		# Create DB if necessary
		db_exists = isfile(self._dbLoc)
		if db_exists:
			log.info('DB_HANDLE: DB {0} found.'.format(self._dbLoc))
			self._conn = sq.connect(self._dbLoc)
			self._cursor = self._conn.cursor()
		else:
			log.info('DB_HANDLE: DB {0} not found. Will be created.'.format(self._dbLoc))
			self.create_DB()

		log.info('DB_HANDLE: Database %s opened.', self._dbLoc)

	def create_DB(self):
		self._conn = sq.connect(self._dbLoc)
		self._cursor = self._conn.cursor()
		self.write_tables()

	def write_tables(self):
		log.info('DB_HANDLE: Performing table creation')
		for (table_name, instruction) in create_instr_SQLite.iteritems():
			(success, error) = commitDBStatement(self.conn, self.cursor, instruction)

	# def __create_table(self, table_name, instruction):
	# 	if self.__table_exists(self.conn, self.cursor, table_name):
	# 		if force:
	# 			log.warning('Dropping Table %s for overwrite.', table_name)
	# 			__drop_table(conn, cursor, table_name)
	# 		else:
	# 			log.error('Table %s already exists', table_name)
	# 			log.error('Databases already exist. If overwriting was your intent, use -mode-TEMP flag to force creation.')
	# 			return 
	# 	log.info("Table %s created.", table_name)
	# 	(success, error) = commitDBStatement(conn, cursor, instruction)

	# def __table_exists(self, table_name):
	# 	'''
	# 	Checks for a table within a database
	# 	PARAMETERS:
	# 				table_name <string> a table name

	# 	RETURNS:
	# 				<bool> whether a table exists
	# 	'''	
	# 	statement = 'select name from sqlite_master where type="table" and name = "{0}";'.format(table_name)
	# 	(success, name) = retrieveDBStatement(self.cursor, statement, expectedColumnCount=1, expectedCount=1)
	# 	return success and (name == table_name) #Second part not strictly necessary, as select will fail if not found

	# def __drop_table(self, table_name):
	# 	'''
	# 	Drops a table from a database
	# 	PARAMETERS:
	# 				table_name <string> a table name

	# 	RETURNS:
	# 				(success, error) <(bool, string)> tuple of whether successful and what error if not
	# 	'''
	# 	statement = 'drop table if exists {0};'.format(table_name)
	# 	return commitDBStatement(self.conn, self.cursor, statement)
