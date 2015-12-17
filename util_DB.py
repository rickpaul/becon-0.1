import sqlite3 as sq
import logging as log
from string import join
from numpy import int64, float64

SQL_NULL = 'NULL' # Sqlite null

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
	return ('insert into ' + table + columnsString + 'values' + valuesString + ';')

########################################Generic Query Construction Code / Update Code
def generateUpdateStatement(table, setColumns, setValues, whereColumns, whereValues):
	setStatements = [(a + '=' + stringify(b)) for (a,b) in zip(setColumns,setValues)]
	whereStatements = [(a + '=' + stringify(b)) for (a,b) in zip(whereColumns,whereValues)]
	setString = join(setStatements,' , ')
	whereString = join(whereStatements,' and ')
	return ('update ' + table + ' set ' + setString + ' where ' + whereString + ';')

########################################Generic Query Construction Code / Select Code
def generateSelectStatement(table, 
							selectColumns=None, 
							selectCount=False, 
							whereColumns=None, whereValues=None, 
							lessThanColumns=None, lessThanValues=None,
							moreThanColumns=None, moreThanValues=None,
							orderBy=None, limit=None):
	if selectCount:
		columnsString = ' count(*) '
	elif selectColumns is None:
		columnsString = ' * '
	else:
		columnsString = ' ' + join(selectColumns,', ') + ' '
	if whereColumns is not None or lessThanColumns is not None or moreThanColumns is not None:
		whereStatements = []
		if whereColumns is not None:
			for (a,b) in zip(whereColumns,whereValues):
				if type(b) is not list:
					whereStatements.append(a + '=' + stringify(b))
				else:
					tempList = [(a + '=' + stringify(c)) for c in b]
					temp = '('
					temp += join(tempList,' or ')
					temp += ')'
					whereStatements.append(temp)
		if lessThanColumns is not None:
			for (a,b) in zip(lessThanColumns,lessThanValues):
				whereStatements.append(a + '<=' + stringify(b))
		if moreThanColumns is not None:
			for (a,b) in zip(moreThanColumns,moreThanValues):
				whereStatements.append(a + '>=' + stringify(b))		
		whereString = ' where ' + join(whereStatements,' and ')
	else:
		whereString = ''
	if orderBy is not None:
		orderByString = ' order by ' + join(orderBy[0],', ') + ' ' + orderBy[1] + ' '
	else:
		orderByString = ''		
	if limit is not None:
		limitString = ' limit ' + str(limit)
	else:
		limitString = ''

	return ('select ' + columnsString + ' from ' + table + whereString + orderByString + limitString + ';')

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
		log.debug('%s Succeeded.')
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
		log.debug('Succeeded.')
		return (True, seriesID)
	except Exception as e:
		log.debug('%s Failed!', statement)
		log.error('%s', e)
		if failSilently:
			return (False, str(e))
		else:
			log.error('FAILED SQL STATEMENT\n{0}\n'.format(statement))
			raise e
