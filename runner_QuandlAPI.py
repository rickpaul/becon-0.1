# TODO: 
# 	perform more checks on data downloaded

# EMF 		From...Import
from 	handle_DataSeries 	import EMF_DataSeries_Handle
from 	handle_CSV 			import EMF_CSV_Handle
from 	handle_QuandlAPI	import EMF_QuandlAPI_Handle
from 	lib_EMF		 		import TEMP_MODE
from 	lib_QuandlAPI		import QuandlCSVColumns, QuandlEditableColumns
from	util_CSV			import boolify
from	util_EMF			import get_EMF_settings
from	util_QuandlAPI		import codify_periodicity
from	util_TimeSet		import dt_epoch_to_str_Y_M_D, dt_str_Y_M_D_Junk_to_epoch
# System 	Import...As
import logging 				as log


class EMF_Quandl_Runner:
	def __init__(self, hndl_DB, mode=TEMP_MODE):
		settings = get_EMF_settings(mode)
		self._hndl_CSV = EMF_CSV_Handle(	settings['QuandlCSVLoc'], 
											columnIndexes=QuandlCSVColumns,
											editableColumns=QuandlEditableColumns)
		self._hndl_DB = hndl_DB

	def __download_dataset_singleSeries(self, 	
										Q_DATABASE_CODE=None,
										Q_DATASET_CODE=None,
										Q_COLUMN_NUM=None, 
										Q_COLLAPSE_INSTR=None, 
										Q_TRANSFORM_INSTR=None,
										start_date=None):
		'''
		TODOS:
					Only Download data that's necessary (i.e. after latest insert) (checking for updates)
		'''
		# Set Quandl Query Parameters
		log.info('QUANDL: Downloading Quandl datafor  {0}:{1}'.format(Q_DATABASE_CODE,Q_DATASET_CODE))
		hndl_Qndl = EMF_QuandlAPI_Handle(Q_DATABASE_CODE, Q_DATASET_CODE)
		# Set Quandl Query Parameters / Column Index
		hndl_Qndl.Instr_Col_Idx = Q_COLUMN_NUM
		# Set Quandl Query Parameters / Collapse
		hndl_Qndl.Instr_Collapse = Q_COLLAPSE_INSTR
		# Set Quandl Query Parameters / Transform
		hndl_Qndl.Instr_Transform = Q_TRANSFORM_INSTR
		# Set Quandl Query Parameters / Max-Date
		hndl_Qndl.Instr_Start_Date = start_date
		# Download Quandl Data
		hndl_Qndl.get_data()
		log.info('QUANDL: Found {0} points from {1} to {2}. Periodicity: {3}'
					.format(hndl_Qndl.Data_Num_Points,
							metadata['Q_EARLIEST_DATE'] if start_date is None else dt_epoch_to_str_Y_M_D(start_date),
							hndl_Qndl.Quandl_Latest_Date,
							hndl_Qndl.Quandl_Periodicity,)
		if metadata['NUM_COLUMNS'] != 2 and Q_COLUMN_NUM == 1:
			log.warning('QUANDL: Found more than one column. Ensure you have right column).')
		# Return
		return (dates, values, metadata)

	def __store_dataset_metadata(self, hndl_Data, metadata):
		hndl_Data.last_refreshed = dt_str_Y_M_D_Junk_to_epoch(metadata['Q_REFRESHED_AT'])
		hndl_Data.periodicity = max(codify_periodicity(metadata['Q_PERIODICITY']), 
									codify_periodicity(metadata('Q_COLLAPSE_INSTR')))
		hndl_Data.original_periodicity = codify_periodicity(metadata['Q_PERIODICITY'])
		hndl_Data.category = metadata['category']
		hndl_Data.subcategory = metadata['subcategory']
		hndl_Data.category_meaning = metadata['category_meaning']
		hndl_Data.is_categorical = boolify(metadata['is_categorical'])
		hndl_Data.geography = metadata['geography']

	def download_CSV_datasets(self):
		# Get Columns for Download
		Qndl_instr_col_names = ['Q_DATABASE_CODE',
								'Q_DATASET_CODE', 
								'Q_COLUMN_NUM', 
								'Q_COLLAPSE_INSTR', 
								'Q_TRANSFORM_INSTR']
		# Get Column Indexes (ints) for Download
		Qndl_instr_col_idxs = [QuandlCSVColumns[x] for x in Qndl_instr_col_names]
		# For Each Desired Dataset (Using CSV Reader)
		for row in self._hndl_CSV:
			# For Each Desired Dataset / Get Quandl Instructions
			download_instr = [row[x] for x in Qndl_instr_col_idxs]
			# For Each Desired Dataset / Create Local Data Handle
			db_name = row[QuandlCSVColumns['db_name']]
			db_ticker = row[QuandlCSVColumns['db_ticker']]
			hndl_Data = EMF_DataSeries_Handle(self._hndl_DB, name=db_name, ticker=db_ticker, insertIfNot=True)
			# For Each Desired Dataset / Read Input CSV Data
			metadata = {
				'geography': row[QuandlCSVColumns['geography']],
				'category': row[QuandlCSVColumns['category_1']],
				'subcategory': row[QuandlCSVColumns['sub_category_1']],
				'category_meaning': row[QuandlCSVColumns['category_1_meaning']],
				'is_categorical': row[QuandlCSVColumns['IS_CATEGORICAL']],
			}
			# For Each Desired Dataset / Update with Previous Input CSV Data
			metadata.update(download_instr)
			# For Each Desired Dataset / Download Quandl Data History
			(dates, values, quandl_metadata) = self.__download_dataset_singleSeries(hndl_Data, *download_instr)
			# For Each Desired Dataset / Save Quandl Data History to Database
			hndl_Data.save_series_db(dates, values)
			# Store Metadata in DB
			metadata.update(quandl_metadata)
			self.__store_dataset_metadata(hndl_Data, metadata)
			# Update CSV
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

