# TODO:
#	Refactor to combine shorter functions

# EMF 		From...Import
from 	lib_CreateDB 	import DataColumnTableLink, WordColumnTableLink, DataColumnTableLink
# EMF 		Import...As
import 	util_DB 			as DB_util
# System 	Import...As
import 	logging 			as log
# System 	From...Import

TICKER = 'ticker'
ID = 'id'

####################################### DATA SERIES + METADATA TABLE
# DATA SERIES TICKER GET FILTERED
def retrieve_DataSeries_Filtered(	cursor, 
									column=ID,
									minDate=None, maxDate=None, 
									periodicity=None, categorical=None,
									limit_=None, order_=False):
	leftTable = 'T_DATA_SERIES'
	rightTable = 'T_DATA_SERIES_METADATA'
	joinCol = 'int_data_series_ID'
	sT = ['T_DATA_SERIES']
	if column == ID:
		sC = ['int_data_series_ID']
	elif column == TICKER:
		sC = ['txt_data_ticker']
	else:
		raise NameError
	# Fill In Where Columns
	wT = []
	wC = []
	wV = []
	wO = []
	args = [minDate, maxDate, periodicity, categorical]
	cols = ['dt_min_data_date', 'dt_max_data_date', 'int_periodicity', 'bool_data_is_categorical']
	ops = ['>=', '<=', '=', '=']
	for (arg, col, op) in zip(args, cols, ops):
		if arg is not None:
			wT.append(DataColumnTableLink[col])
			wC.append(col)
			wV.append(arg)
			wO.append(op)
	# Implement Ordering and Limits
	order_ = ([sC], 'ASC') if order_ else None
	# Generate and Execute Statement
	statement = DB_util.generateJoinedSelectStatement(	leftTable, rightTable, 
														joinCol, joinCol, 
														sC, sT, wC, wV, wT, wO, 
														order_=order_, limit_=limit_)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=1)
	return results # Don't care about success. If not successful, will fail with error


# DATA SERIES TICKER GET ALL
def retrieve_DataSeries_All(cursor, column=ID, limit_=None, order_=False):
	table = 'T_DATA_SERIES'
	# Find Select Column
	if column == ID:
		sC = ['int_data_series_ID']
	elif column == TICKER:
		sC = ['txt_data_ticker']
	else:
		raise NameError
	# Implement Ordering
	order_ = (sC, 'ASC') if order_ else None
	# Generate and Execute Statement
	statement = DB_util.generateSelectStatement(table, selectColumns=sC, order_=order_, limit_=limit_)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=1)
	return results # Don't care about success. If not successful, will fail with error

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
	wO = ['=']*len(wC)
	return DB_util.generateSelectStatement(	table, 
											whereColumns=wC, 
											whereValues=wV, 
											whereOperators=wO,
											selectColumns=sC)
def __get_insert_DataSeriesID_Statement(name=None, ticker=None):
	table = 'T_DATA_SERIES'
	columns = ['txt_data_name', 'txt_data_ticker']
	values = [name, ticker]
	return DB_util.generateInsertStatement(table, columns, values)
def __get_insert_DataSeriesID_Metadata(seriesID):
	table = 'T_DATA_SERIES_METADATA'
	columns = ['int_data_series_ID']
	values = [seriesID]
	return DB_util.generateInsertStatement(table, columns, values)
def retrieve_DataSeriesID(conn, cursor, name=None, ticker=None, insertIfNot=False):
	'''
	
	'''
	statement = __get_retrieve_DataSeriesID_Statement(name=name, ticker=ticker)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=1, expectedCount=1)
	if success:
		return results
	else:
		if insertIfNot:
			assert name is not None
			assert ticker is not None
			log.debug('Series ID Not Found for %s... Creating.', ticker)
			statement = __get_insert_DataSeriesID_Statement(name, ticker)
			(success, rowID_or_Error) = DB_util.commitDBStatement(conn, cursor, statement)
			if success:
				statement = __get_insert_DataSeriesID_Metadata(rowID_or_Error)
				(success, rowID_or_Error) = DB_util.commitDBStatement(conn, cursor, statement)
				return rowID_or_Error # a row ID
			else:
				log.error('Series ID Not Created for %s. Error:\n%s', ticker, rowID_or_Error)
				raise Exception('Series ID Failed to be Created')
		else:
			return None

####################################### DATA SERIES METADATA TABLE
# DATA SERIES METADATA RETRIEVAL/INSERTION
def __get_retrieve_DataSeriesMetaData_Statement(seriesID, columnName):
	table = DataColumnTableLink[columnName]
	sC = [columnName]
	wC = ['int_data_series_ID']
	wV = [seriesID]
	wO = ['=']
	return DB_util.generateSelectStatement(	table, 
											whereColumns=wC, 
											whereValues=wV, 
											whereOperators=wO,
											selectColumns=sC)
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
	(success, rowID_or_Error) = DB_util.commitDBStatement(conn, cursor, statement)
	return success

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

def __get_completeDataHistory_DataHistoryTable_Statement(seriesID, selectCount=False):
	table = 'T_DATA_HISTORY'
	sC = ['dt_date_time','flt_data_value']
	wC = ['int_data_series_ID']
	wV = [seriesID]
	wO = ['=']
	return DB_util.generateSelectStatement(	table, 
										whereColumns=wC, 
										whereValues=wV, 
										whereOperators=wO,
										selectCount=selectCount,
										selectColumns=sC,
										order_=(['dt_date_time'], 'ASC'))
def getCompleteDataHistory_DataHistoryTable(cursor, seriesID, selectCount=False):
	statement = __get_completeDataHistory_DataHistoryTable_Statement(seriesID, selectCount=selectCount)
	expectedCount = 1 if selectCount else None
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=2, expectedCount=expectedCount)
	return results # Don't care about success. If not successful, will fail with error


####################################### WORD SERIES TABLE

# WORD SERIES ID RETRIEVAL/INSERTION
def __get_retrieve_WordSeriesID_Statement(seriesName):
	table = 'T_WORD_SERIES'
	sC = ['int_word_series_ID']
	wC = ['int_word_series_name']
	wV = [seriesName]
	wO = ['=']*len(wC)
	return DB_util.generateSelectStatement(	table, 
											whereColumns=wC, 
											whereValues=wV, 
											whereOperators=wO,
											selectColumns=sC)

def __get_insert_WordSeriesID_Statement(seriesName):
	table = 'T_WORD_SERIES'
	columns = ['int_word_series_name']
	values = [seriesName]
	return DB_util.generateInsertStatement(table, columns, values)

def retrieve_WordSeriesID(conn, cursor, seriesName, insertIfNot=False):
	'''
	
	'''
	statement = __get_retrieve_WordSeriesID_Statement(seriesName)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=1, expectedCount=1)
	if success:
		return results
	else:
		if insertIfNot:
			log.debug('Word Series ID Not Found for %s... Creating.', seriesName)
			statement = __get_insert_WordSeriesID_Statement(seriesName)
			(success, rowID_or_Error) = DB_util.commitDBStatement(conn, cursor, statement)
			if success:
				return rowID_or_Error # a row ID
			else:
				log.error('Series ID Not Created for %s. Error:\n%s', seriesName, rowID_or_Error)
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
	wO = ['=']
	return DB_util.generateSelectStatement(	table, 
											whereColumns=wC, 
											whereValues=wV, 
											whereOperators=wO,
											selectColumns=sC)
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
	wC = ['int_word_master_id']
	wV = [seriesID]
	wO = ['=']*len(wC)
	sC = ['dt_date_time','flt_word_value']
	return DB_util.generateSelectStatement(	table, 
											whereColumns=wC, 
											whereValues=wV, 
											whereOperators=wO,
											selectColumns=sC,
											order_=(['dt_date_time'], 'ASC'))
def getCompleteWordHistory_WordHistoryTable(cursor, seriesID):
	statement = __get_completeWordHistory_WordHistoryTable_Statement(seriesID)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=2, expectedCount=None)
	return results # Don't care about success. If not successful, will fail with error

####################################### WORD STATS TABLE

# WORD STAT INSERTION
def __get_insertStat_WordStatsTable_Statement(indSeriesID, depSeriesID, depFeatureImportance):
	table = 'T_WORD_STATISTICS'
	columns = ['int_word_ind_var_id', 'int_word_dep_var_id', 'adj_dep_feature_importance']
	values = [indSeriesID, depSeriesID, depFeatureImportance]
	return DB_util.generateInsertStatement(table, columns, values)
def insertStat_WordStatsTable(conn, cursor, indSeriesID, depSeriesID, depFeatureImportance):
	statement = __get_insertStat_WordStatsTable_Statement(indSeriesID, depSeriesID, depFeatureImportance)
	(success, err) = DB_util.commitDBStatement(conn, cursor, statement, failSilently=True)
	return success

