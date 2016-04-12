# EMF 		From...Import
from 	handle_EMF					import EMF_Settings_Handle
from 	handle_Logging 			import EMF_Logging_Handle
from 	handle_WordSelector 	import EMF_WordSelector_Handle
from 	handle_WordSet 			import EMF_WordSet_Handle
# from 	lib_DB					import SQLITE_MODE, MYSQL_MODE
# from 	lib_EMF					import TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
from 	lib_Runner_Model 		import PredictorTransformationKeys, ResponseTransformationKeys
from 	util_EMF				import get_DB_Handle

######################## CURRENT RUN PARAMS
settings = EMF_Settings_Handle()

def main():
	DB_MODE = settings.DB_MODE
	EMF_MODE = settings.EMF_MODE
	hndl_Log = EMF_Logging_Handle(mode=EMF_MODE)
	hndl_DB = get_DB_Handle(EMF_mode=EMF_MODE, DB_mode=DB_MODE)
	hndl_WrdSlct = EMF_WordSelector_Handle(hndl_DB)
	hndl_WrdSlct.pred_trns_ptrns 	= PredictorTransformationKeys
	hndl_WrdSlct.resp_trns_ptrns 	= ResponseTransformationKeys
	hndl_WrdSlct.resp_trns_ptrns 	= ['None', 'Futr_Lvl', 'Futr_Change']
	hndl_WrdSlct.resp_data_tickers = ['SP500_RealPrice']
	hndl_WordSet = EMF_WordSet_Handle(hndl_DB)
	hndl_WordSet.resp_words = hndl_WrdSlct.select_resp_words_random()
	hndl_WordSet.pred_words = hndl_WrdSlct.select_pred_words_random()



if __name__ == '__main__':
	main()