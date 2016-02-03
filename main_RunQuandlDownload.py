# EMF 		From...Import
from runner_QuandlAPI 	import EMF_Quandl_Runner
# EMF 		Import...As
import 	lib_EMF 


######################## CURRENT RUN PARAMS
CURRENT_MODE 	= lib_EMF.TEST_MODE

def main():
	QuandlRunner = EMF_Quandl_Runner(CURRENT_MODE)
	QuandlRunner.download_CSV_datasets()

if __name__ == '__main__':
	main()