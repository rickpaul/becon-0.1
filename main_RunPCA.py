# EMF 		From...Import
from 	handle_EMF					import EMF_Settings_Handle
from 	handle_Logging 			import EMF_Logging_Handle
from 	lib_Runner_Model 		import PredictorTransformationKeys, ResponseTransformationKeys # should come from lib_runner_pca?
# from 	lib_DB					import SQLITE_MODE, MYSQL_MODE
# from 	lib_EMF					import TEMP_MODE, TEST_MODE, QA_MODE, PROD_MODE
from 	runner_PCA 				import EMF_PCA_Runner
from 	util_EMF				import get_DB_Handle
# EMF 		Import...As
import 	lib_Runner_PCA

######################## CURRENT RUN PARAMS
settings = EMF_Settings_Handle()
#
CURRENT_TEMPLATE = lib_Runner_PCA.BusCycleTemplate

def main():
	DB_MODE = settings.DB_MODE
	EMF_MODE = settings.EMF_MODE
	hndl_Log = EMF_Logging_Handle(mode=EMF_MODE)
	hndl_DB = get_DB_Handle(EMF_mode=EMF_MODE, DB_mode=DB_MODE)
	runner_PCA = EMF_PCA_Runner(hndl_DB)
	runner_PCA.set_model_from_template(CURRENT_TEMPLATE)
	runner_PCA.add_data()
	runner_PCA.run_PCA()

if __name__ == '__main__':
	main()