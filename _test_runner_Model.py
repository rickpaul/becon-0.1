# EMF 		From...Import
from 	handle_Testing 		import EMF_Testing_Handle
from 	runner_Model 		import EMF_Model_Runner
from 	util_Testing 		import save_test_data_blobs

TestModelTemplate = {
	'independentVariables' : ['clusterNum'],
	'independentTransformations' : ['None'],
	'independentModelCategories' : ['categorical_bounded'],
	'models' : ['ClassDecisionTree'],
	'interpolateDependentData' : False,
	'overrides' : {
		'categorical' : False
	}
}

def main():
	hndl_Test = EMF_Testing_Handle()
	save_test_data(hndl_Test)
	rnnr_Model = EMF_Model_Runner(hndl_Test.hndl_DB)
	rnnr_Model.set_model_from_template(TestModelTemplate)
	rnnr_Model.run_model_batch()

if __name__ == '__main__':
	main()