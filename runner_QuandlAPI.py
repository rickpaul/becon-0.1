# TODO: 
#	move main function into another file

import 	logging as log

import 	lib_QuandlAPI as lib_quandl
from 	handle_DB 			import EMF_Database_Handle		as dbHandle
from 	handle_DataSeries 	import EMF_DataSeries_Handle	as dataHandle
from 	handle_CSV 			import EMF_CSV_Handle 			as csvHandle
from 	handle_QuandlAPI	import EMF_QuandlAPI_Handle 	as quandlHandle

from	util_DB				import retrieveConnection
from	util_Logging		import initializeLog
from	util_EMF			import get_EMF_settings

class EMF_Quandl_Runner:
	def __init__(self, mode):
		settings = get_EMF_settings(mode)
		initializeLog(	logFilePath=settings['logDir'], 
						recordLevel=settings['recordLevel'], 
						recordLog=settings['recordLog'])
		self.CSVHandle = csvHandle(settings['QuandlCSVDir'])
		self.DBHandle = dbHandle(settings['dbDir'])
		self.dataHandle = dataHandle(self.DBHandle.conn, self.DBHandle.cursor)

	def __download_dataset_singleSeries(self, 	Q_DATABASE_CODE, Q_DATASET_CODE, 
												Q_COLUMN_NUM, Q_COLUMN_NAME,
												Q_COLLAPSE_INSTR, Q_TRANSFORM_INSTR,
												db_name, db_ticker):
		'''
		TODOS:
					Only Download data that's necessary (i.e. after latest insert) (checking for updates)
					
		'''
		qndlHandle = quandlHandle(Q_DATABASE_CODE, Q_DATASET_CODE)
		qndlHandle.set_extra_parameter('column_index', Q_COLUMN_NUM)
		qndlHandle.set_extra_parameter('collapse', Q_COLLAPSE_INSTR)
		qndlHandle.set_extra_parameter('transform', Q_TRANSFORM_INSTR)
		(dates, values) = qndlHandle.get_data_history()
		self.dataHandle.set_data_series(name=db_name, ticker=db_ticker, insertIfNot=True)
		self.dataHandle.insert_data_history(dates, values)
		self.dataHandle.unset_data_series()

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
		indexes = [lib_quandl.QuandlCSVColumns[x] for x in columns]
		for row in self.CSVHandle:
			values = [row[x] for x in indexes]
			self.__download_dataset_singleSeries(*values)

def main():
	QuandlRunner = EMF_Quandl_Runner('TEMP')
	QuandlRunner.download_CSV_datasets()

if __name__ == '__main__':
	main()