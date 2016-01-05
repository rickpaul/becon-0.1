# EMF 		From...Import
from 	handle_DB		import EMF_Database_Handle
from 	lib_EMF		 	import TEMP_MODE
from 	util_EMF		import get_EMF_settings
# System 	Import...As
import 	sqlite3 		as sq
import 	logging 		as log
# System 	From...Import
from 	string 			import join
from 	numpy 			import int64, float64

SQL_NULL = 'NULL' # Sqlite null

def get_DB_Handle(mode=TEMP_MODE):
	settings = get_EMF_settings(mode)
	dbLocation = settings['dbLoc']
	return EMF_Database_Handle(dbLocation, deleteDB=False)

########################################Generic Query Construction Code / Helper Code
def stringify(someValue):
	if type(someValue) == bool:
		return str(int(someValue))
	elif type(someValue) == int or type(someValue) == float:
		return str(someValue)
	elif type(someValue) == int64 or type(someValue) == float64:
		return str(someValue)
	elif someValue is None:
		return SQL_NULL
	elif (someValue == SQL_NULL) or (someValue[0] is '"') or (someValue[0] is "'"):
		return someValue
	else:
		return '"' + someValue + '"'

########################################Generic Query Construction Code / Insert Code
def generateInsertStatement(table, columns, values):
	columnsString = ' ( ' + join(columns,', ') + ' ) '
	valuesString = ' ( ' + join([stringify(v) for v in values],', ') + ' ) '
	return 'insert into {0} {1} values {2};'.format(table, columnsString, valuesString)

########################################Generic Query Construction Code / Update Code
def generateUpdateStatement(table, setColumns, setValues, whereColumns, whereValues):
	setStatements = [(a + '=' + stringify(b)) for (a,b) in zip(setColumns,setValues)]
	whereStatements = [(a + '=' + stringify(b)) for (a,b) in zip(whereColumns,whereValues)]
	setString = join(setStatements,' , ')
	whereString = join(whereStatements,' and ')
	return 'update {0} set {1} where {2};'.format(table, setString, whereString)

########################################Generic Query Construction Code / Select Code
def generateSelectStatement(table_, 
							selectColumns=None, selectCount=False, 
							whereColumns=None, whereValues=None, whereOperators=None,
							order_=None, limit_=None):
	if selectCount:
		select_ = 'count(*)'
	elif selectColumns is None:
		select_ = '*'
	else:
		select_ = join(selectColumns,', ')
	if whereColumns is not None:
		where_ = join([(c+op+stringify(v)) for (c, op, v) in zip(whereColumns, whereOperators, whereValues)], ' and ')
	else:
		where_ = '1=1'
	order_ = '' if order_ is None else ('order by ' + join(order_[0],', ') + ' ' + order_[1])
	limit_ = '' if limit_ is None else ('limit ' + str(limit_))
	return 'select {0} from {1} where {2} {3} {4};'.format(select_, table_, where_, order_, limit_)

def generateJoinedSelectStatement(	leftTable, rightTable,
									leftJoinCol, rightJoinCol,
									selectColumns, selectTables,
									whereColumns, whereValues, 
									whereTables, whereOperators,
									order_=None, limit_=None):
	select_ = join([(t+'.'+c) for (t, c) in zip(selectTables, selectColumns)], ', ')
	where_ = join([(t+'.'+c+op+stringify(v)) for (t, c, op, v) in zip(whereTables, whereColumns, whereOperators, whereValues)], ' and ')
	join_ = '{0}.{1}={2}.{3}'.format(leftTable, leftJoinCol, rightTable, rightJoinCol)
	order_ = '' if order_ is None else ('order by ' + join(order_[0],', ') + ' ' + order_[1])
	limit_ = '' if limit_ is None else ('limit ' + str(limit_))
	return 'select {0} from {1} inner join {2} on {3} where {4} {5};'.format(select_, leftTable, rightTable, join_, where_, order_, limit_)


def retrieveDBStatement(cursor, statement, expectedColumnCount=1, expectedCount=None):
	'''
	Performs a select

	PARAMETERS:
	cursor <sqlite3 connection> 
	statement <string> an instruction to perform
	expectedCount <int> a count of expected results
	expectedColumnCount <bool> a count of expected results

	RETURNS:
	(success, error) <(bool, string)> tuple of whether successful and what results

	TODOS:
	Messy. Clean up (need a comprehensive error strategy)
	Implement select for number of columns!
	'''	
	log.debug('Attempting %s ...', statement)
	try:
		cursor.execute(statement)
		results = cursor.fetchall()
	except Exception as e:
		log.debug('%s Failed!', statement)
		log.error('%s', e)
		raise e

	if len(results) == 0:
		return (False, None)

	# Check Count if successful
	if (expectedCount is not None) and (len(results) != expectedCount):
		log.error('%s Had unexpected number of rows (%d expected; %d retrieved)', statement, expectedCount, len(results))
		raise Exception('Unexpected number of rows for query')

	if len(results[0]) != expectedColumnCount:
		log.error('%s Had unexpected number of columns (%d expected; %d retrieved)', statement, expectedColumnCount, len(results[0]))
		raise Exception('Unexpected number of columns for query')

	if expectedColumnCount == 1:
		if expectedCount == 1:
			return (True, results[0][0])
		else:
			return (True, [row[0] for row in results])
	else:
		return (True, results)

def commitDBStatement(conn, cursor, statement, failSilently=False):
	'''
	Performs an atomic commit for insert and update statements

	PARAMETERS:
				conn <sqlite3 connection> 
				cursor <sqlite3 connection> 
				statement <string> an instruction to perform
				failSilently <bool> whether to simply return an error or raise a fresh one

	RETURNS:
				(success, error) <(bool, string or int)> tuple of whether successful and what error (not success), or row id (success)

	TODO:
				Separate returns to not have ambiguity in return
	'''
	log.debug('Attempting %s ...', statement)
	try:
		cursor.execute(statement)
		conn.commit()
		seriesID = cursor.lastrowid
		return (True, seriesID)
	except Exception as e:
		log.debug('%s Failed!', statement)
		log.error('%s', e)
		if failSilently:
			return (False, str(e))
		else:
			log.error('FAILED SQL STATEMENT\n{0}\n'.format(statement))
			raise e
