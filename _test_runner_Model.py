# EMF 		From...Import
from 	handle_Testing 		import EMF_Testing_Handle
from 	lib_EMF				import TEMP_MODE, TEST_MODE
from 	lib_Runner_Model 	import TimeToRecTemplate
from 	lib_TimeSet		 	import DAYS, WEEKS, MONTHS, QUARTERS, YEARS
from 	runner_Model 		import EMF_Model_Runner
from 	util_Testing 		import save_test_data_fn, create_test_data_correlated_returns, create_test_data_linear_change
from 	util_DB				import connect_to_DB


TestModelTemplate = {
	'responseTicker' : ['y'],
	'responseTrns' : ['Futr_Change'],
	'responseKwargs': {
		'PeriodDiff': [1,3,6,9,12],
	# 	'numRanges': [5]
	},
	'responseCanPredict': 1,
	# 'predictorTrns' : [ 'Past_Change'],
	'predictorKwargs': {
		'PeriodDiff': [1,3,6,9,12],
	},
	'models' : ['RegrDecisionTree'],
	'predictorCriteria' : {
		# 'interpolatePredictorData' : False,
		# 'matchResponsePeriodicity' : True,
		# 'periodicity' : qqMONTHS,
		# 'categorical' : False
	}
}

def test_generated_data(mode=TEMP_MODE):
	hndl_Test = EMF_Testing_Handle(mode=mode)
	fn = create_test_data_correlated_returns
	len_ = 100
	(tickers, responseIdx) = save_test_data_fn(hndl_Test, fn, n=len_, numDims=3)
	rnnr_Model = EMF_Model_Runner(hndl_Test.hndl_DB)
	rnnr_Model.set_model_from_template(TestModelTemplate)
	rnnr_Model.train_model_batch()

def test_actual_data(mode=TEST_MODE):
	hndl_DB = connect_to_DB(mode=mode)
	rnnr_Model = EMF_Model_Runner(hndl_DB)
	rnnr_Model.set_model_from_template(TimeToRecTemplate)
	rnnr_Model.train_model_batch()

def main():
	test_generated_data()

if __name__ == '__main__':
	main()