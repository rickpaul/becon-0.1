# TODOS:
#	This isn't actually a test yet.

# EMF 		From...Import
from 	handle_Testing 	import EMF_Testing_Handle
from 	util_Testing 	import save_test_data_fn, create_test_data_correlated_returns, plot_data_series
# EMF 		Import...As
import 	lib_Model

def run_model(hndl_Test, tickers, responseIdx):
	model = lib_Model.EMF_RegressionDecisionTree()
	for (i, t) in enumerate(tickers):
		if i == responseIdx:
			respVar = hndl_Test.retrieve_test_word(t,'None')
			model.add_response_variable(respVar)
		else:
			model.add_predictor_variable(hndl_Test.retrieve_test_word(t,'None'))
	model.run_model()
	plot_data_series(respVar, model)

def main():
	hndl_Test = EMF_Testing_Handle()
	fn = create_test_data_correlated_returns
	(tickers, responseIdx) = save_test_data_fn(hndl_Test, fn, n=100)
	run_model(hndl_Test, tickers, responseIdx)


if __name__ == '__main__':
	main()