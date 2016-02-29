# EMF 		From...Import
from 	handle_JSON 		import EMF_JSON_Handle
from 	handle_Logging 		import EMF_Logging_Handle
from 	runner_Model 		import EMF_Model_Runner
from 	util_Testing 		import save_test_data_fn, create_test_data_correlated_returns
from 	util_DB				import connect_to_DB
# EMF 		Import...As
import 	lib_EMF
import 	lib_Runner_Model

######################## CURRENT RUN PARAMS
CURRENT_MODE 	= lib_EMF.TEST_MODE
CURRENT_MODEL 	= lib_Runner_Model.SP500Template
NUM_TRAIN_RUNS 	= 10

def main():
	hndl_Log = EMF_Logging_Handle(mode=CURRENT_MODE)
	hndl_DB = connect_to_DB(mode=CURRENT_MODE)
	rnnr_Model = EMF_Model_Runner(hndl_DB)
	rnnr_Model.set_model_from_template(CURRENT_MODEL)
	for i in xrange(NUM_TRAIN_RUNS):
		hndl_Res = rnnr_Model.train_model_batch()
	EMF_JSON_Handle().generate_d3_JSON_ParallelCoords(hndl_Res)

if __name__ == '__main__':
	main()