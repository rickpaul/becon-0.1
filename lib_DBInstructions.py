# TODO:
#	Why do minDate and maxDate exist?

# EMF 		From...Import
from 	handle_EMF					import EMF_Settings_Handle
from 	lib_DB					import SQLITE_MODE, MYSQL_MODE
from 	lib_CreateDB 	import DataColumnTableLink, WordColumnTableLink, DataColumnTableLink
# EMF 		Import...As
import 	util_DB 			as DB_util
# System 	Import...As
import 	logging 			as log
# System 	From...Import

TICKER = 'T'
ID = 'ID'

####################################### DATA SERIES + METADATA TABLE
# DATA SERIES TICKER GET FILTERED
def retrieve_DataSeries_Filtered(	cursor, 
									column=ID,
									minDate=None, maxDate=None, 
									atLeastMinDate=None, atLeastMaxDate=None, 
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
	args = [minDate, 
			maxDate, 
			atLeastMinDate, 
			atLeastMaxDate, 
			periodicity, 
			categorical]
	cols = ['dt_min_data_date', 
			'dt_max_data_date', 
			'dt_min_data_date', 
			'dt_max_data_date', 
			'code_local_periodicity', 
			'bool_data_is_categorical']
	ops = ['>=', '<=', '<=', '>=', '=', '=']
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
def __get_insert_DataSeriesID_Statement(name, ticker):
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
	TODO:
				Incorporate idea of rollbacks. 
				rowID_or_Error working differently in mySQL.
				This got messy with fixes.
	'''
	statement = __get_retrieve_DataSeriesID_Statement(name=name, ticker=ticker)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=1, expectedCount=1)
	if success:
		return results
	else:
		if insertIfNot:
			assert name is not None
			assert ticker is not None
			log.info('DATABASE: Series ID Not Found for %s... Creating.', ticker)
			statement = __get_insert_DataSeriesID_Statement(name, ticker)
			(success, rowID_or_Error) = DB_util.commitDBStatement(conn, cursor, statement)
			if success:
				statement = __get_insert_DataSeriesID_Metadata(rowID_or_Error)
				(success, junk_last_id) = DB_util.commitDBStatement(conn, cursor, statement) # mySQL doesn't return good lastrowid when no autoincrement.
				if success:
					return rowID_or_Error # a row ID
		if not success:
			log.error('DATABASE: Series ID Not Created for %s. Error:\n%s', ticker, rowID_or_Error)
			raise Exception('Series ID Failed to be Created')
		else:
			return None
def __get_retrieve_DataSeriesTicker_Statement(seriesID):
	table = 'T_DATA_SERIES'
	sC = ['txt_data_ticker']
	wC = ['int_data_series_ID']
	wV = [seriesID]
	wO = ['=']
	return DB_util.generateSelectStatement(	table, 
											whereColumns=wC, 
											whereValues=wV, 
											whereOperators=wO,
											selectColumns=sC)
def retrieve_DataSeriesTicker(cursor, seriesID):
	statement = __get_retrieve_DataSeriesTicker_Statement(seriesID)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=1, expectedCount=1)
	return results

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
def __get_insertOrUpdateDataPoint_DataHistoryTable_Statement(seriesID, date, value, interpolated, forecast):
	table = 'T_DATA_HISTORY'
	insert_columns = ['int_data_series_ID', 'dt_date_time', 'flt_data_value', 'bool_is_interpolated', 'bool_is_forecast']
	insert_values = [seriesID, date, value, int(interpolated), int(forecast)]
	update_columns = ['flt_data_value', 'bool_is_interpolated', 'bool_is_forecast']
	update_values = [value, int(interpolated), int(forecast)]
	return DB_util.generateInsertOrUpdateStatement_MySQL(table, insert_columns, insert_values, update_columns, update_values)
def insertDataPoint_DataHistoryTable_MySQL(conn, cursor, seriesID, date, value, interpolated=False, forecast=False):
	statement = __get_insertOrUpdateDataPoint_DataHistoryTable_Statement(seriesID, date, value, interpolated, forecast)
	(success, err) = DB_util.commitDBStatement(conn, cursor, statement, failSilently=True)
	return success
def __get_insertDataPoint_DataHistoryTable_Statement(seriesID, date, value, interpolated, forecast):
	table = 'T_DATA_HISTORY'
	columns = ['int_data_series_ID', 'dt_date_time', 'flt_data_value', 'bool_is_interpolated', 'bool_is_forecast']
	values = [seriesID, date, value, int(interpolated), int(forecast)]
	return DB_util.generateInsertStatement(table, columns, values)
def insertDataPoint_DataHistoryTable_SQLite(conn, cursor, seriesID, date, value, interpolated=False, forecast=False):
	statement = __get_insertDataPoint_DataHistoryTable_Statement(seriesID, date, value, interpolated, forecast)
	(success, err) = DB_util.commitDBStatement(conn, cursor, statement, failSilently=True)
	return success
def insertDataPoint_DataHistoryTable(conn, cursor, seriesID, date, value, interpolated=False, forecast=False):
	settings = EMF_Settings_Handle()
	if settings.DB_MODE == SQLITE_MODE:
		return insertDataPoint_DataHistoryTable_SQLite(conn, cursor, seriesID, date, value, interpolated=False, forecast=False)
	elif settings.DB_MODE == MYSQL_MODE:
		return insertDataPoint_DataHistoryTable_MySQL(conn, cursor, seriesID, date, value, interpolated=False, forecast=False)
	else:
		raise NameError('Database Mode not recognized.')

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
			log.info('DATABASE: Word Series ID Not Found for %s... Creating.', seriesName)
			statement = __get_insert_WordSeriesID_Statement(seriesName)
			(success, rowID_or_Error) = DB_util.commitDBStatement(conn, cursor, statement)
			if success:
				return rowID_or_Error # a row ID
			else:
				log.error('DATABASE: Series ID Not Created for %s. Error:\n%s', seriesName, rowID_or_Error)
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
def __get_insertStat_WordStatsTable_Statement(resp_word_ID, pred_word_ID, pred_feature_importance, stat_variance, stat_count):
	table = 'T_WORD_STATISTICS'
	columns = ['int_word_rsp_var_id', 'int_word_prd_var_id', 'adj_prd_feature_importance', 'flt_feat_imp_variance', 'int_feat_imp_count']
	values = [resp_word_ID, pred_word_ID, pred_feature_importance, stat_variance, stat_count]
	return DB_util.generateInsertStatement(table, columns, values)
def insertStat_WordStatsTable(conn, cursor, resp_word_ID, pred_word_ID, pred_feature_importance, stat_variance=0, stat_count=1):
	statement = __get_insertStat_WordStatsTable_Statement(resp_word_ID, pred_word_ID, pred_feature_importance, stat_variance, stat_count)
	(success, err) = DB_util.commitDBStatement(conn, cursor, statement, failSilently=True)
	return success

# WORD STAT RETRIEVAL
def __get_retrieve_Stat_WordStatsTable_Statement(resp_word_ID, pred_word_ID):
	table = 'T_WORD_STATISTICS'
	wC = ['int_word_rsp_var_id', 'int_word_prd_var_id']
	wV = [resp_word_ID, pred_word_ID]
	wO = ['=']*len(wC)
	sC = ['adj_prd_feature_importance', 'flt_feat_imp_variance', 'int_feat_imp_count']
	return DB_util.generateSelectStatement(	table, 
											whereColumns=wC, 
											whereValues=wV, 
											whereOperators=wO,
											selectColumns=sC)
def retrieveStats_WordStatsTable(cursor, resp_word_ID, pred_word_ID):
	statement = __get_retrieve_Stat_WordStatsTable_Statement(resp_word_ID, pred_word_ID)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=3, expectedCount=None)
	return results # Don't care about success. If not successful, will fail with error


# WORD STAT REPLACEMENT
def __get_deleteStats_WordStatsTable_Statement(resp_word_ID, pred_word_ID):
	table = 'T_WORD_STATISTICS'
	wC = ['int_word_rsp_var_id', 'int_word_prd_var_id']
	wV = [resp_word_ID, pred_word_ID]
	return DB_util.generateDeleteStatement(table, wC, wV)
def replaceStats_WordStatsTable(conn, cursor, resp_word_ID, pred_word_ID, pred_feature_importance, stat_variance, stat_count):
	insert_statement = __get_insertStat_WordStatsTable_Statement(resp_word_ID, pred_word_ID, pred_feature_importance, stat_variance, stat_count)
	delete_statement = __get_deleteStats_WordStatsTable_Statement(resp_word_ID, pred_word_ID)
	statement = [delete_statement, insert_statement]
	(success, err) = DB_util.commitDBStatement(conn, cursor, statement, failSilently=True)
	return success

####################################### MODEL STATS TABLE

# MODEL STAT INSERTION
def __get_insertStat_ModelStatsTable_Statement(resp_word_ID, model_ID, model_score, stat_variance, stat_count):
	table = 'T_MODEL_STATISTICS'
	columns = ['int_word_rsp_var_id', 'int_model_id', 'flt_model_score', 'flt_score_variance', 'int_score_count']
	values = [resp_word_ID, model_ID, model_score, stat_variance, stat_count]
	return DB_util.generateInsertStatement(table, columns, values)
def insertStat_ModelStatsTable(conn, cursor, resp_word_ID, model_ID, model_score, stat_variance=0, stat_count=1):
	statement = __get_insertStat_ModelStatsTable_Statement(resp_word_ID, pred_word_ID, pred_feature_importance, stat_variance, stat_count)
	(success, err) = DB_util.commitDBStatement(conn, cursor, statement, failSilently=True)
	return success

# MODEL STAT RETRIEVAL
def __get_retrieve_Stat_ModelStatsTable_Statement(resp_word_ID, model_ID):
	table = 'T_MODEL_STATISTICS'
	wC = ['int_word_rsp_var_id', 'int_model_id']
	wV = [resp_word_ID, model_ID]
	wO = ['=']*len(wC)
	sC = ['flt_model_score', 'flt_score_variance', 'int_score_count']
	return DB_util.generateSelectStatement(	table, 
											whereColumns=wC, 
											whereValues=wV, 
											whereOperators=wO,
											selectColumns=sC)
def retrieveStats_ModelStatsTable(cursor, resp_word_ID, model_ID):
	statement = __get_retrieve_Stat_ModelStatsTable_Statement(resp_word_ID, model_ID)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=3, expectedCount=None)
	return results # Don't care about success. If not successful, will fail with error


####################################### DATA STATS TABLE

# DATA STAT INSERTION
def __get_insertStat_DataStatsTable_Statement(resp_data_ID, pred_data_ID, pred_feature_importance, stat_variance, stat_count):
	table = 'T_DATA_STATISTICS'
	columns = ['int_data_rsp_var_id', 'int_data_prd_var_id', 'adj_prd_feature_importance', 'flt_feat_imp_variance', 'int_feat_imp_count']
	values = [resp_data_ID, pred_data_ID, pred_feature_importance, stat_variance, stat_count]
	return DB_util.generateInsertStatement(table, columns, values)
def insertStat_DataStatsTable(conn, cursor, resp_data_ID, pred_data_ID, pred_feature_importance, stat_variance=0, stat_count=1):
	statement = __get_insertStat_DataStatsTable_Statement(resp_data_ID, pred_data_ID, pred_feature_importance, stat_variance, stat_count)
	(success, err) = DB_util.commitDBStatement(conn, cursor, statement, failSilently=True)
	return success

# DATA STAT RETRIEVAL
def __get_retrieve_Stat_DataStatsTable_Statement(resp_data_ID, pred_data_ID):
	table = 'T_DATA_STATISTICS'
	wC = ['int_data_rsp_var_id', 'int_data_prd_var_id']
	wV = [resp_data_ID, pred_data_ID]
	wO = ['=']*len(wC)
	sC = ['adj_prd_feature_importance', 'flt_feat_imp_variance', 'int_feat_imp_count']
	return DB_util.generateSelectStatement(	table, 
											whereColumns=wC, 
											whereValues=wV, 
											whereOperators=wO,
											selectColumns=sC)
def retrieveStats_DataStatsTable(cursor, resp_data_ID, pred_data_ID):
	statement = __get_retrieve_Stat_DataStatsTable_Statement(resp_data_ID, pred_data_ID)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=3, expectedCount=None)
	return results # Don't care about success. If not successful, will fail with error

# DATA STAT REPLACEMENT
def __get_deleteStats_DataStatsTable_Statement(resp_data_ID, pred_data_ID):
	table = 'T_DATA_STATISTICS'
	wC = ['int_data_rsp_var_id', 'int_data_prd_var_id']
	wV = [resp_data_ID, pred_data_ID]
	return DB_util.generateDeleteStatement(table, wC, wV)
def replaceStats_DataStatsTable(conn, cursor, resp_data_ID, pred_data_ID, pred_feature_importance, stat_variance, stat_count):
	insert_statement = __get_insertStat_DataStatsTable_Statement(resp_data_ID, pred_data_ID, pred_feature_importance, stat_variance, stat_count)
	delete_statement = __get_deleteStats_DataStatsTable_Statement(resp_data_ID, pred_data_ID)
	statement = [delete_statement, insert_statement]
	(success, err) = DB_util.commitDBStatement(conn, cursor, statement, failSilently=True)
	return success

# DATA STAT RETRIEVAL
def __get_retrieveAllStats_DataStatsTable_Statement(resp_data_ID):
	table = 'T_DATA_STATISTICS'
	wC = ['int_data_rsp_var_id']
	wV = [resp_data_ID]
	wO = ['=']
	sC = ['int_data_prd_var_id', 'adj_prd_feature_importance']
	oC = (['adj_prd_feature_importance'],'desc')
	return DB_util.generateSelectStatement(	table, 
											whereColumns=wC, 
											whereValues=wV, 
											whereOperators=wO,
											selectColumns=sC,
											order_=oC)
def retrieveAllStats_DataStatsTable(cursor, resp_data_ID):
	statement = __get_retrieveAllStats_DataStatsTable_Statement(resp_data_ID)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=2, expectedCount=None)
	return results # Don't care about success. If not successful, will fail with error

####################################### DATA ATTRIBUTES TABLE

def __get_retrieveAllStats_DataStatsTable_Statement(resp_data_ID):
	table = 'T_DATA_STATISTICS'
	wC = ['int_data_rsp_var_id']
	wV = [resp_data_ID]
	wO = ['=']
	sC = ['int_data_prd_var_id', 'adj_prd_feature_importance']
	oC = (['adj_prd_feature_importance'],'desc')
	return DB_util.generateSelectStatement(	table, 
											whereColumns=wC, 
											whereValues=wV, 
											whereOperators=wO,
											selectColumns=sC,
											order_=oC)
def retrieveAllStats_DataStatsTable(cursor, resp_data_ID):
	statement = __get_retrieveAllStats_DataStatsTable_Statement(resp_data_ID)
	(success, results) = DB_util.retrieveDBStatement(cursor, statement, expectedColumnCount=2, expectedCount=None)
	return results # Don't care about success. If not successful, will fail with error



