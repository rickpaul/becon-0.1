# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Logging			import EMF_Logging_Handle
from 	handle_EMF					import EMF_Settings_Handle
from 	lib_DBInstructions	import retrieve_DataSeries_All, ID, TICKER
from 	runner_QuandlAPI 		import EMF_Quandl_Runner
from 	util_EMF						import get_DB_Handle

######################## CURRENT RUN PARAMS
settings = EMF_Settings_Handle()

def main():
	DB_MODE = settings.DB_MODE
	EMF_MODE = settings.EMF_MODE
	# Start Log
	hndl_Log = EMF_Logging_Handle(mode=EMF_MODE)
	# Get DB
	hndl_DB = get_DB_Handle(EMF_mode=EMF_MODE, DB_mode=DB_MODE)
	# Get DataSeries
	allTickers = retrieve_DataSeries_All(hndl_DB.cursor, column=TICKER)
	for ticker_ in allTickers:
		hndl_Data = EMF_DataSeries_Handle(hndl_DB, ticker=ticker_)
		hndl_Data


if __name__ == '__main__':
	main()