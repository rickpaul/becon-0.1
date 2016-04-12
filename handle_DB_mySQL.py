# TODO:
# 	Allow Manual Table Writing (Selective Overwrite of Tables)

# EMF 		From...Import
from 	handle_DB 			import EMF_Database_Handle
from 	template_DB 		import EMF_Database_Template
from 	util_DB 			import commitDBStatement, retrieveDBStatement
# EMF 		Import...As
import 	lib_DB
import 	lib_CreateDB
import 	mysql.connector 	as mysq
# System 	Import...As
import 	logging 			as log

class EMF_MySQL_Handle(EMF_Database_Handle, EMF_Database_Template):
	def __init__(self, dbName, deleteDB=False):
		self._dbName = dbName
		self._deleteDB = deleteDB
		self.connect_to_DB()

	def connect_to_DB(self):
		try:
			self._conn = mysq.connect(	host=lib_DB.host, 
										user=lib_DB.username, 
										password=lib_DB.password, 
										database=self._dbName,
										raise_on_warnings=True)
			self._cursor = self._conn.cursor(buffered=True)
		except mysq.Error as err:
			if err.errno == mysq.errorcode.ER_ACCESS_DENIED_ERROR:
				log.error('DB_HANDLE: Database Access Denied.')
				raise err
			elif err.errno == mysq.errorcode.ER_BAD_DB_ERROR:
				log.warning('DB_HANDLE: Database does not exist... Creating')
				self.create_DB()
			else:
				log.error(err)
				raise err
		log.info('DB_HANDLE: Database %s opened.', self._dbName)

	def __del__(self):
		if self._deleteDB:
			statement = 'SET FOREIGN_KEY_CHECKS = 0;'
			commitDBStatement(self.conn, self.cursor, statement)
			statement = 'DROP DATABASE IF EXISTS `{0}`;'.format(self._dbName)
			commitDBStatement(self.conn, self.cursor, statement)
			log.warning('DB_HANDLE: Database %s deleted.', self._dbName)
		self._cursor.close()
		self._conn.close()
		log.info('DB_HANDLE: Database %s closed.', self._dbName)

	def dbName():
		doc = 'The dbName property. Unused.'
		def fget(self):
			return self._dbName
		return locals()
	dbName = property(**dbName())

	def create_DB(self):
		# Create MySQL Connection (Without database)
		try:
			self._conn = mysq.connect(	host=lib_DB.host, 
										user=lib_DB.username, 
										password=lib_DB.password, 
										raise_on_warnings=True)
			self._cursor = self._conn.cursor(buffered=True)
		except mysq.Error as err:
			if err.errno == mysq.errorcode.ER_ACCESS_DENIED_ERROR:
				log.error('DB_HANDLE: Database Access Denied.')
			log.error('DB_HANDLE: '+err)
			raise err
		# Create Database
		statement = 'CREATE DATABASE IF NOT EXISTS `{0}`;'.format(self._dbName)
		commitDBStatement(self.conn, self.cursor, statement)
		log.info('DB_HANDLE: Database %s created (or found).', self._dbName)
		# Assign Database to MySQL Connection
		self._conn.database = self._dbName
		self.write_tables()

	def write_tables(self):
		# Create Tables / Temporarily Turn Off Foreign Key Checks
		statement = 'SET FOREIGN_KEY_CHECKS = 0;'
		commitDBStatement(self.conn, self.cursor, statement)
		# Create Tables / Create Tables
		table_creation_instr = lib_CreateDB.create_instr_MySQL
		for (table_name, create_instr) in table_creation_instr.iteritems():
			self.__create_table(table_name, create_instr)
		# Create Tables / Temporarily Turn Off Foreign Key Checks
		statement = 'SET FOREIGN_KEY_CHECKS = 1;'
		commitDBStatement(self.conn, self.cursor, statement)

	def __table_exists(self, table_name):
		statement = 'SHOW TABLES LIKE "{0}"'.format(table_name)
		(success, name) = retrieveDBStatement(self.cursor, statement, expectedColumnCount=1, expectedCount=1)
		return success and (name == table_name) #Second part not strictly necessary, as select will fail if not found

	def __drop_table(self, table_name):
		statement = 'DROP TABLE `{0}`'.format(table_name)
		(success, error) = commitDBStatement(self.conn, self.cursor, statement)
		if not success:
			log.warning('DB_HANDLE: Failed to drop {0}'.format(table_name))
			log.warning('DB_HANDLE: ' + error)
		else:
			log.warning('DB_HANDLE: Dropped {0}'.format(table_name))

	def __create_table(self, table_name, create_instr, force=False):
		'''
		TODO:
					force is not being used (nothing passing it in)
		'''
		if self.__table_exists(table_name):
			if force:
				log.warning('DB_HANDLE: Dropping Table %s for overwrite.', table_name)
				self.__drop_table(table_name)
			else:
				log.error('DB_HANDLE: Table {0} Exists.'.format(table_name))
				log.error('DB_HANDLE: Failed to create {0}. (Force disabled).'.format(table_name))
				return
		log.info('DB_HANDLE: Creating Table {0}.'.format(table_name))
		(success, error) = commitDBStatement(self.conn, self.cursor, create_instr)
		if not success:
			log.error('DB_HANDLE: Failed to create {0}'.format(table_name))
			log.error('DB_HANDLE: ' + error)
		else:
			log.warning('DB_HANDLE: Created Table {0}.'.format(table_name))
