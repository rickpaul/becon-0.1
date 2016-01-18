#TODOS:
# 	Clean up unused code
# 	Create table for insertion history

creationInstructions = {}
DataColumnTableLink = {}
WordColumnTableLink = {}

createDataSeriesTable = '''
CREATE TABLE T_DATA_SERIES
(
	int_data_series_ID INTEGER UNIQUE NOT NULL PRIMARY KEY,
	txt_data_name TEXT,
	txt_data_ticker TEXT UNIQUE,
	dt_last_updated_history INTEGER, /* when we got the historical data last */
	dt_last_updated_metadata INTEGER /* when we set the metadata last */
);
'''
creationInstructions['T_DATA_SERIES'] = createDataSeriesTable
DataSeriesColumns = [
'txt_data_name',
'txt_data_ticker',
'dt_last_updated_history',
'dt_last_updated_metadata'
]
DataColumnTableLink.update(dict.fromkeys(DataSeriesColumns,'T_DATA_SERIES'))

createDataSeriesMetadataTable = '''
CREATE TABLE T_DATA_SERIES_METADATA
(
	int_data_series_ID INTEGER UNIQUE NOT NULL PRIMARY KEY,
	dt_min_data_date INTEGER, /* earliest stored data point */
	dt_max_data_date INTEGER, /* latest stored data point */
	code_local_periodicity INTEGER,
	code_original_periodicity INTEGER,
	bool_data_is_categorical INTEGER, /* False if data is continuous */
	FOREIGN KEY (int_data_series_ID) REFERENCES T_DATA_SERIES (int_data_series_ID)
);
'''
creationInstructions['T_DATA_SERIES_METADATA'] = createDataSeriesMetadataTable
DataSeriesColumns = [
'dt_min_data_date',
'dt_max_data_date',
'code_local_periodicity',
'code_original_periodicity',
'bool_data_is_categorical'
]
DataColumnTableLink.update(dict.fromkeys(DataSeriesColumns,'T_DATA_SERIES_METADATA'))

createDataHistoryTable = '''
CREATE TABLE T_DATA_HISTORY
(
	int_data_series_ID INTEGER,
	dt_date_time INTEGER,
	flt_data_value REAL,
	bool_is_interpolated INTEGER,
	bool_is_forecast INTEGER,
	UNIQUE (int_data_series_ID, dt_date_time) ON CONFLICT REPLACE,
	FOREIGN KEY (int_data_series_ID) REFERENCES T_DATA_SERIES (int_data_series_ID)
);
'''
creationInstructions['T_DATA_HISTORY'] = createDataHistoryTable
DataHistoryColumns = [
# None: No metadata
]
DataColumnTableLink.update(dict.fromkeys(DataHistoryColumns,'T_DATA_HISTORY'))

createWordSeriesTable = '''
CREATE TABLE T_WORD_SERIES
(
	int_word_series_ID INTEGER UNIQUE NOT NULL PRIMARY KEY,
	int_word_series_name TEXT,
	int_data_series_ID INTEGER,
	int_transformation_hash INTEGER,
	bool_word_is_stored INTEGER DEFAULT 0,
	dt_history_last_accessed INTEGER,
	UNIQUE (int_word_series_name),
	FOREIGN KEY (int_data_series_ID) REFERENCES T_DATA_SERIES (int_data_series_ID)
);
'''
creationInstructions['T_WORD_SERIES'] = createWordSeriesTable
WordSeriesColumns = [
'int_data_series_ID',
'int_transformation_hash',
'bool_word_is_stored',
'dt_history_last_accessed',
]
WordColumnTableLink.update(dict.fromkeys(WordSeriesColumns,'T_WORD_SERIES'))

createWordHistoryTable = '''
CREATE TABLE T_WORD_HISTORY
(
	int_word_master_id INTEGER,
	dt_date_time INTEGER,
	flt_word_value REAL,
	UNIQUE (int_word_master_id, dt_date_time) ON CONFLICT REPLACE,
	FOREIGN KEY (int_word_master_id) REFERENCES T_WORD_SERIES (int_word_master_id)
);
'''
creationInstructions['T_WORD_HISTORY'] = createWordHistoryTable
WordHistoryColumns = [
# None: No metaword
]
WordColumnTableLink.update(dict.fromkeys(WordHistoryColumns,'T_WORD_HISTORY'))

createWordStatsTable = '''
CREATE TABLE T_WORD_STATISTICS
(
	int_word_ind_var_id INTEGER,
	int_word_dep_var_id INTEGER,
	adj_dep_feature_importance REAL,
	FOREIGN KEY (int_word_ind_var_id) REFERENCES T_WORD_SERIES (int_word_master_id)
	FOREIGN KEY (int_word_dep_var_id) REFERENCES T_WORD_SERIES (int_word_master_id)
);
'''
creationInstructions['T_WORD_STATISTICS'] = createWordStatsTable
WordStatsColumns = [
# None: No metaword
]
WordColumnTableLink.update(dict.fromkeys(WordStatsColumns,'T_WORD_STATISTICS'))


# createWordEffectivenessTable = '''
# CREATE TABLE  T_WORD_EFFECTIVENESS
# 	int_predictor_word_ID INTEGER NOT NULL,
# 	int_response_word_ID INTEGER NOT NULL,
# 	flt_correlation ? REAL,
# 	flt_information_content ? REAL,
# 	flt_average_marginal_modeling_effectiveness REAL, /* when this data is removed from model, how much does model suffer? */
# 	flt_average_raw_modeling_effectiveness REAL, /* when this data is the complete model, how much does model work? */
# 	FOREIGN KEY (int_predictor_word_ID) REFERENCES T_DATA_SERIES (int_word_series_ID),
# 	FOREIGN KEY (int_response_word_ID) REFERENCES T_DATA_SERIES (int_word_series_ID),
# '''



creationInstructionsOverride = {
			# 'T_DATA_SERIES':createDataSeriesTable,
			# 'T_DATA_HISTORY':createDataHistoryTable,
			# 'T_TRANSFORMATIONS':createDataTransformationsTable
		}
