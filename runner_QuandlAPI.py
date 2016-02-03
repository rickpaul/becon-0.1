# TODO: 
# 	perform more checks on data downloaded

# EMF 		From...Import
from 	handle_DB		 	import EMF_Database_Handle
from 	handle_DataSeries 	import EMF_DataSeries_Handle
from 	handle_CSV 			import EMF_CSV_Handle
from 	handle_QuandlAPI	import EMF_QuandlAPI_Handle
from 	handle_Logging		import EMF_Logging_Handle
from 	lib_EMF		 		import TEMP_MODE
from 	lib_QuandlAPI		import QuandlCSVColumns, QuandlEditableColumns
from	util_CSV			import boolify
from	util_EMF			import get_EMF_settings
from	util_QuandlAPI		import codify_periodicity
from	util_TimeSet		import dt_epoch_to_str_Y_M_D, dt_str_Y_M_D_Junk_to_epoch
# System 	Import...As
import logging 				as log


class EMF_Quandl_Runner:
	def __init__(self, mode=TEMP_MODE):
		settings = get_EMF_settings(mode)
		self.hndl_Log = EMF_Logging_Handle(mode=mode)
		self.hndl_CSV = EMF_CSV_Handle(	settings['QuandlCSVLoc'], 
										columnIndexes=QuandlCSVColumns,
										editableColumns=QuandlEditableColumns)
		self.hndl_DB = EMF_Database_Handle(settings['dbLoc'])
		
		

	def __download_dataset_singleSeries(self, 	hndl_Data,
												Q_DATABASE_CODE, Q_DATASET_CODE, 
												Q_COLUMN_NUM, Q_COLUMN_NAME,
												Q_COLLAPSE_INSTR, Q_TRANSFORM_INSTR):
		'''
		TODOS:
					Only Download data that's necessary (i.e. after latest insert) (checking for updates)
					
		'''
		# Set Data Handle
		max_date = hndl_Data.max_date
		# Set Quandl Query Parameters
		hndl_Qndl = EMF_QuandlAPI_Handle(Q_DATABASE_CODE, Q_DATASET_CODE)
		if max_date is not None:
			hndl_Qndl.set_extra_parameter('start_date', dt_epoch_to_str_Y_M_D(max_date))
		hndl_Qndl.set_extra_parameter('column_index', Q_COLUMN_NUM)
		hndl_Qndl.set_extra_parameter('collapse', Q_COLLAPSE_INSTR)
		hndl_Qndl.set_extra_parameter('transform', Q_TRANSFORM_INSTR)
		log.info('QUANDL: Downloading data for {0}'.format(hndl_Data))
		# Download Quandl Data
		(dates, values, metadata) = hndl_Qndl.get_data()
		log.info('QUANDL: Found {0} points from {1} to {2} ({3} periodicity).'
					.format(metadata['NUM_POINTS'],
							metadata['Q_EARLIEST_DATE'] if max_date is None else dt_epoch_to_str_Y_M_D(max_date),
							metadata['Q_LATEST_DATE'],
							metadata['Q_PERIODICITY']),)
		log.info('QUANDL: Found {0} for {1}'.format(metadata['Q_NAME'], hndl_Data))
		if metadata['NUM_COLUMNS'] != 2 and Q_COLUMN_NUM == 1:
			log.warning('QUANDL: Found more than one column. Ensure you have right column).')
		# Insert Data History
		hndl_Data.save_series_db(dates, values)
		return metadata


	def __store_dataset_metadata(self, hndl_Data, metadata):
		hndl_Data.last_refreshed = dt_str_Y_M_D_Junk_to_epoch(metadata['Q_REFRESHED_AT'])
		raise NotImplementedError('the line below hasn\'t been tested.')
		hndl_Data.periodicity = max(codify_periodicity(metadata['Q_PERIODICITY']), 
									codify_periodicity(metadata('Q_COLLAPSE_INSTR')))
		hndl_Data.original_periodicity = codify_periodicity(metadata['Q_PERIODICITY'])
		hndl_Data.category = metadata['category']
		hndl_Data.subcategory = metadata['subcategory']
		hndl_Data.category_meaning = metadata['category_meaning']
		hndl_Data.is_categorical = boolify(metadata['is_categorical'])
		hndl_Data.geography = metadata['geography']

	def download_CSV_datasets(self):
		# IMPORTANT: ORDER OF columns MUST MATCH ORDER OF PARAMETERS FOR...
		# ...download_dataset_singleSeries (FN ABOVE).
		columns = [	'Q_DATABASE_CODE',
					'Q_DATASET_CODE', 
					'Q_COLUMN_NUM', 
					'Q_COLUMN_NAME', 
					'Q_COLLAPSE_INSTR', 
					'Q_TRANSFORM_INSTR']
		indexes = [QuandlCSVColumns[x] for x in columns]
		for row in self.hndl_CSV:
			download_instr = [row[x] for x in indexes]
			# Create Data Handle
			db_name = row[QuandlCSVColumns['db_name']]
			db_ticker = row[QuandlCSVColumns['db_ticker']]
			hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, name=db_name, ticker=db_ticker, insertIfNot=True)
			# Get CSV Data
			metadata = {
				'geography': row[QuandlCSVColumns['geography']],
				'category': row[QuandlCSVColumns['category_1']],
				'subcategory': row[QuandlCSVColumns['sub_category_1']],
				'category_meaning': row[QuandlCSVColumns['category_1_meaning']],
				'is_categorical': row[QuandlCSVColumns['IS_CATEGORICAL']],
			}
			metadata.update(download_instr)
			# Get Quandl Data
			quandl_metadata = self.__download_dataset_singleSeries(hndl_Data, *download_instr)
			metadata.update(quandl_metadata)
			# Store Metadata in DB
			self.__store_dataset_metadata(hndl_Data, metadata)
			# Update CSV
			for (key, val) in quandl_metadata.iteritems():
				try:
					str(val).decode("utf-8") # To prevent writing bad values
					self.hndl_CSV.change_current_row(val, columnName=key)
				except UnicodeDecodeError, e:
					log.warning('QUANDL: Unicode error writing to csv')
					log.warning('QUANDL: Row:{0} Col:{1}'.format(row, key))
				except UnicodeEncodeError, e:
					log.warning('QUANDL: Unicode error writing to csv')
					log.warning('QUANDL: Row:{0} Col:{1}'.format(row, key))
		self.hndl_CSV.write_to_csv()

