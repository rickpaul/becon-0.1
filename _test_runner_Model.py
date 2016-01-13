# EMF 		From...Import
from 	handle_Testing 		import EMF_Testing_Handle
from 	lib_EMF				import TEMP_MODE, TEST_MODE
from 	lib_Runner_Model 	import TestModelTemplate
from 	runner_Model 		import EMF_Model_Runner
from 	util_Testing 		import save_test_data_fn, create_test_data_correlated_returns
from 	util_CreateDB		import connect_DB


def test_generated_data():
	hndl_Test = EMF_Testing_Handle()
	fn = create_test_data_correlated_returns
	len_ = 100
	(tickers, responseIdx) = save_test_data_fn(hndl_Test, fn, n=len_)
	rnnr_Model = EMF_Model_Runner(hndl_Test.hndl_DB)
	rnnr_Model.set_model_from_template(TestModelTemplate)
	rnnr_Model.train_model_batch()


def test_actual_data(mode=TEST_MODE):
	hndl_Test = EMF_Testing_Handle(mode=mode)
	rnnr_Model = EMF_Model_Runner(hndl_Test.hndl_DB)
	rnnr_Model.set_model_from_template(TestModelTemplate)
	rnnr_Model.train_model_batch()

def main():
	test_actual_data(mode=TEST_MODE)

if __name__ == '__main__':
	main() 