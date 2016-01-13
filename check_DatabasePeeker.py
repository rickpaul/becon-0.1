# TODO:
# 	Protect from attacks (i.e. no drops or anything)
# 		If we wnt to. The whole point of this is to be able to do stuff like that.

# EMF 		From...Import
from lib_EMF		import TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
from util_CreateDB 	import connect_DB
from string 		import find, join, lower
from pprint 		import pprint


########################################Database Helper Code / Outward-Facing Simple Statement Executor
def __executeSimpleDatabaseStatement(hndl_DB, statement, showCols=True):
	c = hndl_DB.cursor_()
	cn = hndl_DB.conn_()
	statement = statement.replace('\t', '')
	statement = statement.replace('\n', '')
	statement = statement.strip()
	queryType = lower(statement[0:find(statement,' ')])
	#TODO: Fix to ignore whitespace/handle it better. Consider using regexes.
	if queryType == 'select':
		if showCols:
			tableNameStart = find(statement,'from ') + 5
			tableNameEnd = find(statement,' ',tableNameStart)
			if tableNameEnd == -1: tableNameEnd = len(statement)
			tableName = statement[tableNameStart:tableNameEnd]
			pragmaCommand = 'pragma table_info("' + tableName + '")'
			c.execute(pragmaCommand)
			pragma = c.fetchall()
			print 'COLUMN NAMES:'
			print [col[1] for col in pragma]
			print 'COLUMN TYPES:'	
			print [col[2] for col in pragma]
		print 'VALUES:'
		c.execute(statement)
		results = c.fetchall()
		if len(results) == 0:
			print 'NOTHING FOUND'
		else:
			pprint(results)
	elif queryType == 'insert' or queryType == 'update':
		c.execute(statement)
		cn.commit()
	else:
		raise NameError('simple database query type not recognized')


########################################Database Helper Code / Outward-facing Table Peeking for Debugging
def __peekTable(hndl_DB, tableName, displayPragma=False, limit=10):
	c = hndl_DB.cursor_()
	# Print Table Length
	viewLengthCommand = 'select count(*) from ' + tableName
	c.execute(viewLengthCommand)
	print 'There are ' + str(c.fetchall()[0][0]) + ' rows in ' + tableName
	# Get Table Column Names and Types
	pragmaCommand = 'pragma table_info("' + tableName + '")'
	c.execute(pragmaCommand)
	pragma = c.fetchall()
	#		(pragma columns are as follows:)
	#		(cid,name,type,notnull,dflt_value,pk)
	columnNames = [col[1] for col in pragma]
	columnTypes = [col[2] for col in pragma]
	if displayPragma:
		print '(pragma columns are as follows:)'
		print '(column-id,name,type,not-null,default-value,primary-key)'
		pprint(pragma)
	# Print First Few Rows of Table		
	viewFirstFewCommand = 'select * from ' + tableName + ' limit ' + str(limit)
	c.execute(viewFirstFewCommand)
	firstFew = c.fetchall()
	print columnTypes
	print columnNames
	pprint(firstFew)

def __databasePicker(mode=TEMP_MODE):
	errorCount = 10
	while errorCount >= 0:
		try:
			print '\n\nChoose Database: (1)TEMP (2)TEST (3)QA (4)PROD'
			print '\tCurrent Database is {0}'.format(mode)
			db = raw_input('\tPlease enter a database number if you desire, or "!q" to quit:  ')
			if db == '!q':
				return None
			modes = [TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE]
			mode = modes[int(db)-1]
			return connect_DB(mode=mode)
		except Exception as e:
			print 'ERROR: '
			print e
			print 'Will auto-quit after another {0} errors'.format(errorCount)
			errorCount -= 1
	return None

def __tablePeeker(hndl_DB):
	c = hndl_DB.cursor_()
	errorCount = 10
	table = ''
	while errorCount >= 0:
		try:
			print '\n\nChoose Table or "!q" to quit:'
			viewTableCommand = "select name from sqlite_master where type = 'table'"
			c.execute(viewTableCommand)
			tables = c.fetchall()
			print '\tCurrent Tables Are: '
			for t in tables: print '\t\t{0}'.format(t[0])
			table = raw_input('\tPlease enter a table name:  ')
			if table == '!q':
				return None
			pragma = raw_input('\tDisplay pragma? Type 1/0 for yes/no:  ')
			pragma = int(pragma)
			__peekTable(hndl_DB, table, displayPragma=pragma)
		except Exception as e:
			print 'ERROR: '
			print e
			print 'Will auto-quit after another {0} errors'.format(errorCount)
			errorCount -= 1
	return None

def __commandReader(hndl_DB):
	errorCount = 10
	while errorCount >= 0:
		print '\n\nEnter A Command?:'
		statement = raw_input('\nType Any Command, or "!q" to quit. Finish a command in "!r" to skip.:\n')
		if statement == '!q':
			return None
		if statement == '' or statement[-2:]=='!r':
			continue
		else:
			try:
				__executeSimpleDatabaseStatement(hndl_DB, statement, showCols=True)
			except Exception as e:
				print 'ERROR: '
				print e
				print 'Will auto-quit after another {0} errors'.format(errorCount)
				errorCount -= 1
	return None

if __name__ == '__main__':
	hndl_DB = __databasePicker()
	if hndl_DB is not None:
		__tablePeeker(hndl_DB)
		__commandReader(hndl_DB)


