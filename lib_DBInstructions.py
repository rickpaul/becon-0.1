# TODO:
#	Refactor to combine shorter functions
# EMF 		From...Import
from 	lib_CreateDB 	import DataColumnTableLink, WordColumnTableLink
# EMF 		Import...As
import 	util_DB 			as DB_util
# System 	Import...As
import 	logging 			as log
# System 	From...Import



####################################### DATA SERIES TABLE

# DATA SERIES ID RETRIEVAL/INSERTION
def __get_retrieve_DataSeriesID_Statement(name=None, ticker=None):
	table = 'T_DATA_SERIES'
	sC = ['int_data_series_ID']
	wC = []
	wV = []
	if ticker is not None:
		wC.append('txt_data_ticker')
		wV.append(ticker)
	if name is not None:
		wC.append('txt_data_name')
		wV.append(name)
	return DB_util.generateSelectStatement(	table, whereColumns=wC, whereValues=wV, selectColumns=sC)
def __get_insert_DataSeriesID_Statement(name=None, ticker=None):
	table = 'T_DATA_SERIES'
	columns = ['txt_data_name', 'txt_data_ticker']
	values = [name, ticker]
	return DB_util.generateInsertStatement(table, columns, values)
def retrieve_DataSeriesID(conn, cursor, name=None, ticker=None, insertIfNot=False):
	'''
	
	'''
	statement = __get_retrieve_DataSeriesID_Statement(name=name, ticker=ticker)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=1, expectedCount=1)
	if success:
		if (type(results) == int):
			return results
		else:
			log.error('Multiple Series ID Found for %s, %s', ticker, name)
			raise Exception('Data Series table has duplicate entries!')
	else:
		if insertIfNot:
			assert name is not None
			assert ticker is not None
			log.debug('Series ID Not Found for %s... Creating.', ticker)
			statement = __get_insert_DataSeriesID_Statement(name, ticker)
			(success, rowID_or_Error) = DB_util.commitDBStatement(conn, cursor, statement)
			if success:
				return rowID_or_Error # a row ID
			else:
				log.error('Series ID Not Created for %s. Error:\n%s', ticker, rowID_or_Error)
				raise Exception('Series ID Failed to be Created')
		else:
			return None

# DATA SERIES METADATA RETRIEVAL/INSERTION
def __get_retrieve_DataSeriesMetaData_Statement(seriesID, columnName):
	table = DataColumnTableLink[columnName]
	sC = [columnName]
	wC = ['int_data_series_ID']
	wV = [seriesID]
	return DB_util.generateSelectStatement(	table, whereColumns=wC, whereValues=wV, selectColumns=sC)
def retrieve_DataSeriesMetaData(cursor, columnName, seriesID):
	'''
	
	'''
	statement = __get_retrieve_DataSeriesMetaData_Statement(seriesID, columnName)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=1, expectedCount=1)
	return results # Don't care about success. If not successful, will fail with error

def __get_update_DataSeriesMetaData_Statement(seriesID, columnName, value):
	table = DataColumnTableLink[columnName]
	setColumns = [columnName]
	setValues = [value]
	whereColumns = ['int_data_series_ID']
	whereValues = [seriesID]
	return DB_util.generateUpdateStatement(table, setColumns, setValues, whereColumns, whereValues)

def update_DataSeriesMetaData(conn, cursor, columnName, value, seriesID):
	'''

	'''
	statement = __get_update_DataSeriesMetaData_Statement(seriesID, columnName, value)
	DB_util.commitDBStatement(conn, cursor, statement)

####################################### DATA HISTORY TABLE

def __get_insertDataPoint_DataHistoryTable_Statement(seriesID, date, value, interpolated, forecast):
	table = 'T_DATA_HISTORY'
	columns = ['int_data_series_ID', 'dt_date_time', 'flt_data_value', 'bool_is_interpolated', 'bool_is_forecast']
	values = [seriesID, date, value, int(interpolated), int(forecast)]
	return DB_util.generateInsertStatement(table, columns, values)
def insertDataPoint_DataHistoryTable(conn, cursor, seriesID, date, value, interpolated=False, forecast=False):
	statement = __get_insertDataPoint_DataHistoryTable_Statement(seriesID, date, value, interpolated, forecast)
	(success, err) = DB_util.commitDBStatement(conn, cursor, statement, failSilently=True)
	return success

def __get_completeDataHistory_DataHistoryTable_Statement(seriesID):
	table = 'T_DATA_HISTORY'
	whereColumns = ['int_data_series_ID']
	whereValues = [seriesID]
	selectColumns = ['dt_date_time','flt_data_value']
	return DB_util.generateSelectStatement(	table, 
												whereColumns=whereColumns, 
												whereValues=whereValues, 
												selectColumns=selectColumns,
												orderBy=(['dt_date_time'], 'ASC'))
def getCompleteDataHistory_DataHistoryTable(cursor, seriesID):
	statement = __get_completeDataHistory_DataHistoryTable_Statement(seriesID)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=2, expectedCount=None)
	return results # Don't care about success. If not successful, will fail with error


####################################### WORD SERIES TABLE

# WORD SERIES ID RETRIEVAL/INSERTION
def __get_retrieve_WordSeriesID_Statement(dataSeriesID, transformationHash):
	table = 'T_WORD_SERIES'
	sC = ['int_word_series_ID']
	wC = ['int_data_series_ID', 'int_transformation_hash']
	wV = [dataSeriesID, transformationHash]
	return DB_util.generateSelectStatement(	table, whereColumns=wC, whereValues=wV, selectColumns=sC)

def __get_insert_WordSeriesID_Statement(dataSeriesID, transformationHash):
	table = 'T_WORD_SERIES'
	columns = ['int_data_series_ID', 'int_transformation_hash']
	values = [dataSeriesID, transformationHash]
	return DB_util.generateInsertStatement(table, columns, values)

def retrieve_WordSeriesID(conn, cursor, dataSeriesID, transformationHash, insertIfNot=False):
	'''
	
	'''
	statement = __get_retrieve_WordSeriesID_Statement(dataSeriesID, transformationHash)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=1, expectedCount=1)
	if success:
		if (len(results) == 1):
			return int(results)
		else:
			log.error('Multiple Word Series ID Found for %s, %s', dataSeriesID, transformationHash)
			raise Exception('Word Series table has duplicate entries!')
	else:
		if insertIfNot:
			log.debug('Word Series ID Not Found for %s, %s... Creating.', dataSeriesID, transformationHash)
			statement = __get_insert_WordSeriesID_Statement(dataSeriesID, transformationHash)
			(success, rowID_or_Error) = DB_util.commitDBStatement(conn, cursor, statement)
			if success:
				return rowID_or_Error # a row ID
			else:
				log.error('Series ID Not Created for %s, %s. Error:\n%s', dataSeriesID, transformationHash, rowID_or_Error)
				raise Exception('Word Series ID Failed to be Created')
		else:
			return None

####################################### WORD SERIES METADATA RETRIEVAL/INSERTION

# RETRIEVE WORD METADATA
def __get_retrieve_WordSeriesMetaData_Statement(seriesID, columnName):
	table = WordColumnTableLink[columnName]
	sC = [columnName]
	wC = ['int_word_series_ID']
	wV = [seriesID]
	return DB_util.generateSelectStatement(	table, whereColumns=wC, whereValues=wV, selectColumns=sC)
def retrieve_WordSeriesMetaData(cursor, columnName, seriesID):
	'''
	
	'''
	statement = __get_retrieve_WordSeriesMetaData_Statement(seriesID, columnName)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=1, expectedCount=1)
	return results # Don't care about success. If not successful, will fail with error
# UPDATE WORD METADATA
def __get_update_WordSeriesMetaData_Statement(seriesID, columnName, value):
	table = WordColumnTableLink[columnName]
	setColumns = [columnName]
	setValues = [value]
	whereColumns = ['int_word_series_ID']
	whereValues = [seriesID]
	return DB_util.generateUpdateStatement(table, setColumns, setValues, whereColumns, whereValues)
def update_WordSeriesMetaData(conn, cursor, columnName, value, seriesID):
	'''

	'''
	statement = __get_update_WordSeriesMetaData_Statement(seriesID, columnName, value)
	DB_util.commitDBStatement(conn, cursor, statement)

####################################### WORD HISTORY TABLE

# WORD HISTORY INSERTION
def __get_insertWordPoint_WordHistoryTable_Statement(seriesID, date, value):
	table = 'T_WORD_HISTORY'
	columns = ['int_word_master_id', 'dt_date_time', 'flt_word_value']
	values = [seriesID, date, value]
	return DB_util.generateInsertStatement(table, columns, values)
def insertWordPoint_WordHistoryTable(conn, cursor, seriesID, date, value):
	statement = __get_insertWordPoint_WordHistoryTable_Statement(seriesID, date, value)
	(success, err) = DB_util.commitDBStatement(conn, cursor, statement, failSilently=True)
	return success
# WORD HISTORY RETRIEVAL
def __get_completeWordHistory_WordHistoryTable_Statement(seriesID):
	table = 'T_WORD_HISTORY'
	whereColumns = ['int_word_master_id']
	whereValues = [seriesID]
	selectColumns = ['dt_date_time','flt_word_value']
	return DB_util.generateSelectStatement(	table, 
												whereColumns=whereColumns, 
												whereValues=whereValues, 
												selectColumns=selectColumns,
												orderBy=(['dt_date_time'], 'ASC'))
def getCompleteWordHistory_WordHistoryTable(cursor, seriesID):
	statement = __get_completeWordHistory_WordHistoryTable_Statement(seriesID)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=2, expectedCount=None)
	return results # Don't care about success. If not successful, will fail with error

