# EMF 		From...Import
from 	handle_Logging 			import EMF_Logging_Handle
from 	lib_Runner_Model 		import PredictorTransformationKeys, ResponseTransformationKeys # should come from lib_runner_pca?
from 	runner_PCA 				import EMF_PCA_Runner
from 	util_DB					import connect_to_DB
# EMF 		Import...As
import 	lib_EMF
import 	lib_Runner_PCA


CURRENT_MODE = lib_EMF.TEST_MODE
CURRENT_TEMPLATE = lib_Runner_PCA.BusCycleTemplate

def main(hndl_DB):
	runner_PCA = EMF_PCA_Runner(hndl_DB)
	runner_PCA.set_model_from_template(CURRENT_TEMPLATE)
	runner_PCA.add_data()
	runner_PCA.run_PCA()

if __name__ == '__main__':
	hndl_Log = EMF_Logging_Handle(mode=CURRENT_MODE)
	hndl_DB = connect_to_DB(mode=CURRENT_MODE)
	main(hndl_DB)