#TODOS:
# 	Clean up unused code
# 	Create table for insertion history

DataColumnTableLink = {}
WordColumnTableLink = {}

######################################### SQLite Instructions
create_instr_SQLite = {}

create_T_DATA_SERIES_SQLite = '''
CREATE TABLE T_DATA_SERIES
(
	int_data_series_ID INTEGER UNIQUE NOT NULL PRIMARY KEY,
	txt_data_name TEXT,
	txt_data_ticker TEXT UNIQUE,
	dt_last_updated_history INTEGER, /* when we set the historical data last */
	dt_last_updated_metadata INTEGER /* when we set the metadata last */
);
'''
create_instr_SQLite['T_DATA_SERIES'] = create_T_DATA_SERIES_SQLite
modifiable_columns = [
'txt_data_name',
'txt_data_ticker',
'dt_last_updated_history',
'dt_last_updated_metadata'
]
DataColumnTableLink.update(dict.fromkeys(modifiable_columns,'T_DATA_SERIES'))

create_T_DATA_SERIES_METADATA_SQLite = '''
CREATE TABLE T_DATA_SERIES_METADATA
(
	int_data_series_ID INTEGER UNIQUE NOT NULL PRIMARY KEY,
	dt_min_data_date INTEGER, /* earliest stored data point */
	dt_max_data_date INTEGER, /* latest stored data point */
	dt_last_refreshed_date INTEGER, /* when latest data point was provided */
	txt_Quandl_dataset TEXT,
	txt_Quandl_database TEXT,
	txt_geography TEXT,
	txt_category TEXT,
	txt_subcategory TEXT,
	txt_category_meaning TEXT,
	code_local_periodicity INTEGER,
	code_original_periodicity INTEGER,
	bool_data_is_categorical INTEGER, /* False if data is continuous */
	FOREIGN KEY (int_data_series_ID) REFERENCES T_DATA_SERIES (int_data_series_ID)
);
'''
create_instr_SQLite['T_DATA_SERIES_METADATA'] = create_T_DATA_SERIES_METADATA_SQLite
modifiable_columns = [
'dt_min_data_date',
'dt_max_data_date',
'dt_last_refreshed_date',
'txt_geography',
'txt_category',
'txt_subcategory',
'txt_category_meaning',
'code_local_periodicity',
'code_original_periodicity',
'bool_data_is_categorical',
'txt_Quandl_dataset',
'txt_Quandl_database'
]
DataColumnTableLink.update(dict.fromkeys(modifiable_columns,'T_DATA_SERIES_METADATA'))

create_T_DATA_HISTORY_SQLite = '''
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
create_instr_SQLite['T_DATA_HISTORY'] = create_T_DATA_HISTORY_SQLite

create_T_WORD_SERIES_SQLite = '''
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
create_instr_SQLite['T_WORD_SERIES'] = create_T_WORD_SERIES_SQLite
modifiable_columns = [
'int_data_series_ID',
'int_transformation_hash',
'bool_word_is_stored',
'dt_history_last_accessed',
]
WordColumnTableLink.update(dict.fromkeys(modifiable_columns,'T_WORD_SERIES'))

create_T_WORD_HISTORY_SQLite = '''
CREATE TABLE T_WORD_HISTORY
(
	int_word_series_id INTEGER,
	dt_date_time INTEGER,
	flt_word_value REAL,
	UNIQUE (int_word_series_id, dt_date_time) ON CONFLICT REPLACE,
	FOREIGN KEY (int_word_series_id) REFERENCES T_WORD_SERIES (int_word_series_id)
);
'''
create_instr_SQLite['T_WORD_HISTORY'] = create_T_WORD_HISTORY_SQLite

create_T_WORD_STATISTICS_SQLite = '''
CREATE TABLE T_WORD_STATISTICS
(
	int_word_rsp_var_id INTEGER, /* Response Variable ID */
	int_word_prd_var_id INTEGER, /* Predictor Variable ID */
	adj_prd_feature_importance REAL, /* Predictor Variable Adjusted Feature Importance */
	flt_feat_imp_variance REAL,
	int_feat_imp_count INTEGER,
	FOREIGN KEY (int_word_rsp_var_id) REFERENCES T_WORD_SERIES (int_word_series_id)
	FOREIGN KEY (int_word_prd_var_id) REFERENCES T_WORD_SERIES (int_word_series_id)
);
'''
create_instr_SQLite['T_WORD_STATISTICS'] = create_T_WORD_STATISTICS_SQLite

create_T_MODEL_STATISTICS_SQLite = '''
CREATE TABLE T_MODEL_STATISTICS
(
	int_word_rsp_var_id INTEGER, /* Response Variable ID */
	int_model_id INTEGER,
	flt_model_score REAL,
	flt_score_variance REAL,
	int_score_count INTEGER,
	FOREIGN KEY (int_word_rsp_var_id) REFERENCES T_WORD_SERIES (int_word_series_id)
);
'''
create_instr_SQLite['T_MODEL_STATISTICS'] = create_T_MODEL_STATISTICS_SQLite

create_T_DATA_STATISTICS_SQLite = '''
CREATE TABLE T_DATA_STATISTICS
(
	int_data_rsp_var_id INTEGER, /* Response Variable ID */
	int_data_prd_var_id INTEGER, /* Predictor Variable ID */
	adj_prd_feature_importance REAL, /* Predictor Variable Adjusted Feature Importance */
	flt_feat_imp_variance REAL,
	int_feat_imp_count INTEGER,
	FOREIGN KEY (int_data_rsp_var_id) REFERENCES T_DATA_SERIES (int_data_series_ID)
	FOREIGN KEY (int_data_prd_var_id) REFERENCES T_DATA_SERIES (int_data_series_ID)	
);
'''
create_instr_SQLite['T_DATA_STATISTICS'] = create_T_DATA_STATISTICS_SQLite

create_T_DATA_ATTRIBUTES_SQLite = '''
CREATE TABLE T_DATA_ATTRIBUTES
(
	int_data_series_id INTEGER, /* Response Variable ID */
	txt_attribute_type REAL, /* Threshhold above/below which we care */
	flt_data_threshhold REAL, /* Threshhold above/below which we care */
	flt_data_time_frame REAL, /* Only for rising/falling values */
	code_time_frame_units INTEGER,
	int_feat_imp_count INTEGER,
	FOREIGN KEY (int_data_series_id) REFERENCES T_DATA_SERIES (int_data_series_ID)
);
'''
create_instr_SQLite['T_DATA_ATTRIBUTES'] = create_T_DATA_ATTRIBUTES_SQLite

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

create_instr_SQLite_Override = {
			# 'T_DATA_SERIES':create_T_DATA_SERIES_SQLite,
			# 'T_DATA_HISTORY':create_T_DATA_HISTORY_SQLite,
			# 'T_WORD_HISTORY':create_T_WORD_HISTORY_SQLite,
			# 'T_TRANSFORMATIONS':createDataTransformationsTable
			# 'T_WORD_STATISTICS': create_T_WORD_STATISTICS_SQLite,
			# 'T_DATA_STATISTICS': create_T_DATA_STATISTICS_SQLite,
			# 'T_MODEL_STATISTICS': create_T_MODEL_STATISTICS_SQLite,
		}


######################################### MySQL Instructions

create_instr_MySQL = {}

create_T_DATA_SERIES_MySQL = '''
CREATE TABLE `T_DATA_SERIES`
(
	`int_data_series_ID` int(32) UNSIGNED NOT NULL AUTO_INCREMENT,
	`txt_data_name` varchar(255),
	`txt_data_ticker` varchar(255),
	`dt_last_updated_history` int(32), /* when we set the historical data last */
	`dt_last_updated_metadata` int(32), /* when we set the metadata last */
	PRIMARY KEY (`int_data_series_ID`),
	UNIQUE KEY (`txt_data_ticker`)
) ENGINE=InnoDB;
'''
create_instr_MySQL['T_DATA_SERIES'] = create_T_DATA_SERIES_MySQL
modifiable_columns = [
'txt_data_name',
'txt_data_ticker',
'dt_last_updated_history',
'dt_last_updated_metadata'
]
DataColumnTableLink.update(dict.fromkeys(modifiable_columns,'T_DATA_SERIES'))

create_T_DATA_SERIES_METADATA_MySQL = '''
CREATE TABLE `T_DATA_SERIES_METADATA`
(
	`int_data_series_ID` int(32) UNSIGNED NOT NULL,
	`dt_min_data_date` int(32), /* earliest stored data point */
	`dt_max_data_date` int(32), /* latest stored data point */
	`dt_last_refreshed_date` int(32), /* when latest data point was provided */
	`txt_Quandl_Dataset` varchar(255),
	`txt_Quandl_Database` varchar(255),
	`txt_geography` varchar(255),
	`txt_category` varchar(255),
	`txt_subcategory` varchar(255),
	`txt_category_meaning` varchar(255),
	`code_local_periodicity` int(32),
	`code_original_periodicity` int(32),
	`bool_data_is_categorical` tinyint(1), /* False if data is continuous */
	PRIMARY KEY (`int_data_series_ID`),
	CONSTRAINT `fk_T_DATA_SERIES_METADATA_ID` FOREIGN KEY (`int_data_series_ID`)
		REFERENCES `T_DATA_SERIES` (`int_data_series_ID`)
) ENGINE=InnoDB;
'''
create_instr_MySQL['T_DATA_SERIES_METADATA'] = create_T_DATA_SERIES_METADATA_MySQL
modifiable_columns = [
'dt_min_data_date',
'dt_max_data_date',
'dt_last_refreshed_date',
'txt_geography',
'txt_category',
'txt_subcategory',
'txt_category_meaning',
'code_local_periodicity',
'code_original_periodicity',
'bool_data_is_categorical',
'txt_Quandl_dataset',
'txt_Quandl_database'
]
DataColumnTableLink.update(dict.fromkeys(modifiable_columns,'T_DATA_SERIES_METADATA'))

create_T_DATA_HISTORY_MySQL = '''
CREATE TABLE `T_DATA_HISTORY`
(
	`int_data_series_ID` int(32) UNSIGNED NOT NULL,
	`dt_date_time` int(32) NOT NULL,
	`flt_data_value` double NOT NULL,
	`bool_is_interpolated` int(32),
	`bool_is_forecast` int(32),
	PRIMARY KEY (`int_data_series_ID`, `dt_date_time`),
	CONSTRAINT `fk_T_DATA_HISTORY_ID` FOREIGN KEY (`int_data_series_ID`)
		REFERENCES `T_DATA_SERIES` (`int_data_series_ID`)
) ENGINE=InnoDB;
'''
create_instr_MySQL['T_DATA_HISTORY'] = create_T_DATA_HISTORY_MySQL

create_T_WORD_SERIES_MySQL = '''
CREATE TABLE T_WORD_SERIES
(
	`int_word_series_ID` int(32) UNSIGNED NOT NULL AUTO_INCREMENT,
	`int_word_series_name` varchar(255) NOT NULL,
	`int_data_series_ID` int(32) UNSIGNED NOT NULL,
	`int_transformation_hash` int(32),
	`bool_word_is_stored` int(32) DEFAULT 0,
	`dt_history_last_accessed` int(32),
	PRIMARY KEY (`int_word_series_ID`),
	UNIQUE KEY (`int_word_series_name`),
	CONSTRAINT `fk_T_WORD_SERIES_ID` FOREIGN KEY (`int_data_series_ID`)
		REFERENCES `T_DATA_SERIES` (`int_data_series_ID`)
) ENGINE=InnoDB;
'''
create_instr_MySQL['T_WORD_SERIES'] = create_T_WORD_SERIES_MySQL
modifiable_columns = [
'int_data_series_ID',
'int_transformation_hash',
'bool_word_is_stored',
'dt_history_last_accessed',
]
WordColumnTableLink.update(dict.fromkeys(modifiable_columns,'T_WORD_SERIES'))

create_T_WORD_HISTORY_MySQL = '''
CREATE TABLE T_WORD_HISTORY
(
	`int_word_series_ID` int(32) UNSIGNED NOT NULL,
	`dt_date_time` int(32) NOT NULL,
	`flt_word_value` double NOT NULL,
	PRIMARY KEY (`int_word_series_id`, `dt_date_time`),
	CONSTRAINT `fk_T_WORD_HISTORY_ID` FOREIGN KEY (`int_word_series_ID`)
		REFERENCES `T_WORD_SERIES` (`int_word_series_ID`)
) ENGINE=InnoDB;
'''
create_instr_MySQL['T_WORD_HISTORY'] = create_T_WORD_HISTORY_MySQL

create_T_WORD_STATISTICS_MySQL = '''
CREATE TABLE T_WORD_STATISTICS
(
	`int_word_rsp_var_id` int(32) UNSIGNED NOT NULL, /* Response Variable ID */
	`int_word_prd_var_id` int(32) UNSIGNED NOT NULL, /* Predictor Variable ID */
	`adj_prd_feature_importance` double, /* Predictor Variable Adjusted Feature Importance */
	`flt_feat_imp_variance` double,
	`int_feat_imp_count` int(32),
	CONSTRAINT `fk_T_WORD_STATISTICS_ID_1` FOREIGN KEY (`int_word_rsp_var_id`)
		REFERENCES `T_WORD_SERIES` (`int_word_series_ID`),
	CONSTRAINT `fk_T_WORD_STATISTICS_ID_2` FOREIGN KEY (`int_word_prd_var_id`)
		REFERENCES `T_WORD_SERIES` (`int_word_series_ID`)
) ENGINE=InnoDB;
'''
create_instr_MySQL['T_WORD_STATISTICS'] = create_T_WORD_STATISTICS_MySQL

create_T_MODEL_STATISTICS_MySQL = '''
CREATE TABLE T_MODEL_STATISTICS
(
	`int_word_rsp_var_id` int(32) UNSIGNED NOT NULL, /* Response Variable ID */
	`int_model_id` int(32),
	`flt_model_score` double,
	`flt_score_variance` double,
	`int_score_count` int(32),
	CONSTRAINT `fk_T_MODEL_STATISTICS_ID` FOREIGN KEY (`int_word_rsp_var_id`)
		REFERENCES `T_WORD_SERIES` (`int_word_series_ID`)
) ENGINE=InnoDB;
'''
create_instr_MySQL['T_MODEL_STATISTICS'] = create_T_MODEL_STATISTICS_MySQL

create_T_DATA_STATISTICS_MySQL = '''
CREATE TABLE T_DATA_STATISTICS
(
	`int_data_rsp_var_id` int(32) UNSIGNED NOT NULL, /* Response Variable ID */
	`int_data_prd_var_id` int(32) UNSIGNED NOT NULL, /* Predictor Variable ID */
	`adj_prd_feature_importance` double, /* Predictor Variable Adjusted Feature Importance */
	`flt_feat_imp_variance` double,
	`int_feat_imp_count` int(32),
	CONSTRAINT `fk_T_DATA_STATISTICS_ID_1` FOREIGN KEY (`int_data_rsp_var_id`)
		REFERENCES `T_DATA_SERIES` (`int_data_series_ID`),
	CONSTRAINT `fk_T_DATA_STATISTICS_ID_2` FOREIGN KEY (`int_data_prd_var_id`)
		REFERENCES `T_DATA_SERIES` (`int_data_series_ID`)
) ENGINE=InnoDB;
'''
create_instr_MySQL['T_DATA_STATISTICS'] = create_T_DATA_STATISTICS_MySQL

create_T_DATA_ATTRIBUTES_MySQL = '''
CREATE TABLE T_DATA_ATTRIBUTES
(
	`int_data_series_id` int(32) UNSIGNED NOT NULL, /* Response Variable ID */
	`txt_attribute_type` varchar(255), /* Above/Below/Rising/Falling, for now */
	`flt_data_threshhold` double, /* Threshhold above/below which we care */
	`int_data_time_frame` int(32), /* Only for rising/falling values */
	`code_time_frame_units` int(32), /* Only for rising/falling values. Could change to set */
	CONSTRAINT `fk_T_DATA_STATISTICS_ID` FOREIGN KEY (`int_data_series_id`)
		REFERENCES `T_DATA_SERIES` (`int_data_series_ID`)
) ENGINE=InnoDB;
'''
create_instr_MySQL['T_DATA_ATTRIBUTES'] = create_T_DATA_ATTRIBUTES_MySQL


create_instr_MySQL_Override = {
			# 'T_DATA_SERIES':create_T_DATA_SERIES_MySQL,
			# 'T_DATA_HISTORY':create_T_DATA_HISTORY_MySQL,
			# 'T_WORD_HISTORY':create_T_WORD_HISTORY_MySQL,
			# 'T_TRANSFORMATIONS':createDataTransformationsTable
			# 'T_WORD_STATISTICS': create_T_WORD_STATISTICS_MySQL,
			# 'T_DATA_STATISTICS': create_T_DATA_STATISTICS_MySQL,
			# 'T_MODEL_STATISTICS': create_T_MODEL_STATISTICS_MySQL,
		}