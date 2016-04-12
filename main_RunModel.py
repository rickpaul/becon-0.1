# EMF 		From...Import
from 	handle_EMF					import EMF_Settings_Handle
from 	handle_JSON 			import EMF_JSON_Handle
from 	handle_Logging 			import EMF_Logging_Handle
# from 	lib_DB					import SQLITE_MODE, MYSQL_MODE
# from 	lib_EMF					import TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
from 	runner_Model 			import EMF_Model_Runner
from 	util_EMF				import get_DB_Handle
from 	util_Testing 			import save_test_data_fn, create_test_data_correlated_returns
# EMF 		Import...As
import 	lib_Runner_Model

######################## CURRENT RUN PARAMS
settings = EMF_Settings_Handle()
#
CURRENT_MODEL 	= lib_Runner_Model.SP500Template
NUM_TRAIN_RUNS 	= 10

def main():
	DB_MODE = settings.DB_MODE
	EMF_MODE = settings.EMF_MODE
	hndl_Log = EMF_Logging_Handle(mode=EMF_MODE)
	hndl_DB = get_DB_Handle(EMF_mode=EMF_MODE, DB_mode=DB_MODE)
	rnnr_Model = EMF_Model_Runner(hndl_DB)
	rnnr_Model.set_model_from_template(CURRENT_MODEL)
	for i in xrange(NUM_TRAIN_RUNS):
		hndl_Res = rnnr_Model.train_model_batch()
	EMF_JSON_Handle().generate_d3_JSON_ParallelCoords(hndl_Res)

if __name__ == '__main__':
	main()