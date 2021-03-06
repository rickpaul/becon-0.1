# EMF 		From...Import
from 	handle_Logging			import EMF_Logging_Handle
from 	handle_EMF					import EMF_Settings_Handle
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
	# Start Quandl_Runner
	rnnr_Quandl = EMF_Quandl_Runner(hndl_DB, EMF_mode=EMF_MODE)
	# Start Download
	rnnr_Quandl.download_CSV_datasets()

if __name__ == '__main__':
	main()