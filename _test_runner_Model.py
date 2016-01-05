# EMF 		From...Import
from 	handle_Testing 		import EMF_Testing_Handle
from 	runner_Model 		import EMF_Model_Runner
from 	util_Testing 		import save_test_data_fn, create_test_data_correlated_returns
from 	lib_Runner_Model 	import TestModelTemplate

def main():
	hndl_Test = EMF_Testing_Handle()
	fn = create_test_data_correlated_returns
	len_ = 200
	(tickers, responseIdx) = save_test_data_fn(hndl_Test, fn, n=len_)
	rnnr_Model = EMF_Model_Runner(hndl_Test.hndl_DB)
	rnnr_Model.set_model_from_template(TestModelTemplate)
	rnnr_Model.run_model_batch()

if __name__ == '__main__':
	main() 