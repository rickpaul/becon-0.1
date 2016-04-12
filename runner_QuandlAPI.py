# TODO: 
# 	Perform checks on data downloaded
# 	How to deal with Instr_Start_Date? We keep setting it to Null on accident, rather than using default 

# EMF 		From...Import
from 	handle_DataSeries 	import EMF_DataSeries_Handle
from 	handle_CSV 			import EMF_CSV_Handle
from 	handle_QuandlAPI	import EMF_QuandlAPI_Handle
from 	lib_EMF		 		import TEMP_MODE
from 	lib_QuandlAPI		import QuandlCSVColumns, QuandlEditableColumns
from 	lib_QuandlAPI		import QuandlDnldCols, QuandlDnldColIdxs
from 	lib_QuandlAPI		import USE_DEFAULT
from	util_CSV			import boolify
from	util_EMF			import get_EMF_settings
from	util_QuandlAPI		import codify_periodicity
from	util_TimeSet		import dt_epoch_to_str_Y_M_D, dt_str_Y_M_D_Junk_to_epoch
# System 	Import...As
import logging 				as log

class EMF_Quandl_Runner:
	def __init__(self, hndl_DB, EMF_mode=TEMP_MODE):
		settings = get_EMF_settings(EMF_mode)
		self._hndl_CSV = EMF_CSV_Handle(	settings['QuandlCSVLoc'], 
											columnIndexes=QuandlCSVColumns,
											editableColumns=QuandlEditableColumns)
		self._hndl_DB = hndl_DB

	def __download_dataset_singleSeries(self, 	
										Q_DATABASE_CODE=None,
										Q_DATASET_CODE=None,
										Q_COLUMN_NUM=USE_DEFAULT, 
										Q_COLLAPSE_INSTR=USE_DEFAULT, 
										Q_TRANSFORM_INSTR=USE_DEFAULT,
										start_date=USE_DEFAULT):
		'''
		TODOS:
					Only Download data that's necessary (i.e. after latest insert) (checking for updates)
		'''
		# Set Quandl Query Parameters
		log.info('QUANDL: Downloading Quandl data for (Database|Dataset): ({0}|{1})'.format(Q_DATABASE_CODE,Q_DATASET_CODE))
		hndl_Qndl = EMF_QuandlAPI_Handle(Q_DATABASE_CODE, Q_DATASET_CODE)
		# Set Quandl Query Parameters / Column Index
		hndl_Qndl.Instr_Col_Idx = Q_COLUMN_NUM
		# Set Quandl Query Parameters / Collapse
		hndl_Qndl.Instr_Collapse = Q_COLLAPSE_INSTR
		# Set Quandl Query Parameters / Transform
		hndl_Qndl.Instr_Transform = Q_TRANSFORM_INSTR
		# Set Quandl Query Parameters / Start Date
		hndl_Qndl.Instr_Start_Date = start_date
		# Download Quandl Data
		hndl_Qndl.get_data()
		try:
			log.info('QUANDL: Found {0} points from {1} to {2}. Periodicity: {3}'
						.format(hndl_Qndl.Data_Num_Points,
								hndl_Qndl.Data_Earliest_Date,
								hndl_Qndl.Data_Latest_Date,
								hndl_Qndl.Quandl_Periodicity))
			if hndl_Qndl.Data_Num_Columns != 2 and Q_COLUMN_NUM == 1:
				log.warning('QUANDL: Found more than one column. Ensure you have right column).')
		except Exception:
			pass
		# Return
		return hndl_Qndl

	def __store_dataset_metadata(self, hndl_Data, hndl_Qndl, CSV_Metadata):
		hndl_Data.last_refreshed = dt_str_Y_M_D_Junk_to_epoch(hndl_Qndl.Quandl_Latest_Refresh) # Should make this take the time, not junk it.
		hndl_Data.periodicity = codify_periodicity(hndl_Qndl.Data_Periodicity) # Kind of silly to de-code into string and re-encode
		hndl_Data.original_periodicity = codify_periodicity(hndl_Qndl.Quandl_Periodicity)
		#
		hndl_Data.category = CSV_Metadata['category_1']
		hndl_Data.subcategory = CSV_Metadata['sub_category_1']
		hndl_Data.category_meaning = CSV_Metadata['category_1_meaning']
		hndl_Data.is_categorical = boolify(CSV_Metadata['IS_CATEGORICAL'])
		hndl_Data.geography = CSV_Metadata['geography']
		#
		hndl_Data.Quandl_dataset = hndl_Qndl.Quandl_Dataset
		hndl_Data.Quandl_database = hndl_Qndl.Quandl_Database

	def download_CSV_datasets(self):
		MetadataCols = [	'geography',
							'category_1',
							'sub_category_1',
							'category_1_meaning',
							'IS_CATEGORICAL']
		MetadataColIdxs = [QuandlCSVColumns[x] for x in MetadataCols]
		# For Each Desired Dataset (Using CSV Reader)
		for row in self._hndl_CSV:
			# Download Quandl Data History and Metadata
			download_instr = dict([(name, row[idx]) for (name, idx) in zip(QuandlDnldCols, QuandlDnldColIdxs)])
			hndl_Qndl = self.__download_dataset_singleSeries(**download_instr)
			# For Each Desired Dataset / If No Error
			if hndl_Qndl.error is None:
				# For Each Desired Dataset / If No Error / Create Local Data Handle
				db_name = row[QuandlCSVColumns['db_name']]
				db_ticker = row[QuandlCSVColumns['db_ticker']]
				hndl_Data = EMF_DataSeries_Handle(self._hndl_DB, name=db_name, ticker=db_ticker, insertIfNot=True)
				# For Each Desired Dataset / If No Error / Read Input CSV Data
				metadata = dict([(name, row[idx]) for (name, idx) in zip(MetadataCols, MetadataColIdxs)])
				# For Each Desired Dataset / If No Error / Store Data History in DB
				hndl_Data.save_series_db(hndl_Qndl.dates, hndl_Qndl.values)
				# For Each Desired Dataset / If No Error / Store Metadata in DB
				self.__store_dataset_metadata(hndl_Data, hndl_Qndl, metadata)
				# For Each Desired Dataset / If No Error / Update CSV Variables
				quandl_metadata = {
					'Q_COLUMN_NAME' : hndl_Qndl.Data_Chosen_Column,
					'Q_REFRESHED_AT' : hndl_Qndl.Quandl_Latest_Refresh,
					'Q_EARLIEST_DATE' : hndl_Qndl.Quandl_Earliest_Date,
					'Q_LATEST_DATE' : hndl_Qndl.Quandl_Latest_Date,
					'Q_PERIODICITY' : hndl_Qndl.Quandl_Periodicity,
					'Q_DESCRIPTION' : hndl_Qndl.Quandl_Description,
					'Q_NAME' : hndl_Qndl.Data_Chosen_Column,
					'NUM_COLUMNS' : hndl_Qndl.Data_Num_Columns,
					'NUM_POINTS' : hndl_Qndl.Data_Num_Points,
					'ERROR' : hndl_Qndl.error
				}
			else:
				# For Each Desired Dataset / If Error / Update CSV Variables
				quandl_metadata = {
					'ERROR' : hndl_Qndl.error
				}
			# For Each Desired Dataset / Write Results to CSV
			for (key, val) in quandl_metadata.iteritems():
				try:
					str(val).decode('utf-8') # To prevent writing bad values
					self._hndl_CSV.change_current_row(val, columnName=key)
				except UnicodeDecodeError, e:
					log.warning('QUANDL: Unicode error writing to csv')
					log.warning('QUANDL: Row:{0} Col:{1}'.format(row, key))
				except UnicodeEncodeError, e:
					log.warning('QUANDL: Unicode error writing to csv')
					log.warning('QUANDL: Row:{0} Col:{1}'.format(row, key))
		self._hndl_CSV.write_to_csv()

