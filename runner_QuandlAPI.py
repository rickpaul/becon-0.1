# TODO: 
#	move main function into another file

# EMF 		From...Import
from 	handle_DB		 	import EMF_Database_Handle
from 	handle_DataSeries 	import EMF_DataSeries_Handle
from 	handle_CSV 			import EMF_CSV_Handle
from 	handle_QuandlAPI	import EMF_QuandlAPI_Handle
from 	handle_Logging		import EMF_Logging_Handle
# from 	util_CreateDB	 	import create_DB
from	util_EMF			import get_EMF_settings
from 	lib_EMF		 		import TEMP_MODE
from 	lib_QuandlAPI		import QuandlCSVColumns, QuandlEditableColumns
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
		

	def __download_dataset_singleSeries(self, 	Q_DATABASE_CODE, Q_DATASET_CODE, 
												Q_COLUMN_NUM, Q_COLUMN_NAME,
												Q_COLLAPSE_INSTR, Q_TRANSFORM_INSTR,
												db_name, db_ticker):
		'''
		TODOS:
					Only Download data that's necessary (i.e. after latest insert) (checking for updates)
					
		'''
		hndl_Qndl = EMF_QuandlAPI_Handle(Q_DATABASE_CODE, Q_DATASET_CODE)
		hndl_Qndl.set_extra_parameter('column_index', Q_COLUMN_NUM)
		hndl_Qndl.set_extra_parameter('collapse', Q_COLLAPSE_INSTR)
		hndl_Qndl.set_extra_parameter('transform', Q_TRANSFORM_INSTR)
		(dates, values, metadata) = hndl_Qndl.get_data()
		hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, name=db_name, ticker=db_ticker, insertIfNot=True)
		hndl_Data.save_series_to_db(dates, values)
		return metadata

	def download_CSV_datasets(self):
		# IMPORTANT: ORDER OF columns MUST MATCH ORDER OF PARAMETERS FOR download_dataset_singleSeries
		columns = [	'Q_DATABASE_CODE',
					'Q_DATASET_CODE', 
					'Q_COLUMN_NUM', 
					'Q_COLUMN_NAME', 
					'Q_COLLAPSE_INSTR', 
					'Q_TRANSFORM_INSTR', 
					'db_name', 
					'db_ticker']
		indexes = [QuandlCSVColumns[x] for x in columns]
		for row in self.hndl_CSV:
			values = [row[x] for x in indexes]
			metadata = self.__download_dataset_singleSeries(*values)
			for (key, val) in metadata.iteritems():
				self.hndl_CSV.change_current_row(val, columnName=key)
		self.hndl_CSV.write_to_csv()

def main():
	from lib_EMF import TEST_MODE
	QuandlRunner = EMF_Quandl_Runner(TEST_MODE)
	QuandlRunner.download_CSV_datasets()

if __name__ == '__main__':
	main()