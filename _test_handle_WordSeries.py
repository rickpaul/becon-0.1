# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Testing 			import EMF_Testing_Handle
from 	handle_Transformation	import EMF_Transformation_Handle
from 	handle_WordSeries		import EMF_WordSeries_Handle
from 	runner_Model 			import EMF_Model_Runner
from 	util_Testing 			import save_test_data_fn, create_test_data_correlated_returns, plot_data_series

def main():
	hndl_Test = EMF_Testing_Handle()
	fn = create_test_data_correlated_returns
	(tickers, responseIdx) = save_test_data_fn(hndl_Test, fn)
	hndl_Data = EMF_DataSeries_Handle(hndl_Test.hndl_DB, ticker=tickers[0])
	trnsKwargs={'PeriodDiff': 12}
	# hndl_Trns = EMF_Transformation_Handle('RateOfChange')
	# hndl_Trns.set_extra_parameter('PeriodDiff', 12)
	# hndl_Word = EMF_WordSeries_Handle(hndl_Test.hndl_DB, hndl_Data, hndl_Trns)
	# plot_data_series(hndl_Data, hndl_Word)
	# hndl_Trns = EMF_Transformation_Handle('RateOfChange_Cat')
	# hndl_Trns.set_extra_parameter('PeriodDiff', 12)
	# hndl_Word = EMF_WordSeries_Handle(hndl_Test.hndl_DB, hndl_Data, hndl_Trns)
	# plot_data_series(hndl_Data, hndl_Word)
	hndl_Trns = EMF_Transformation_Handle('Past_Change_NormRd', trnsKwargs)
	hndl_Word_Chng = EMF_WordSeries_Handle(hndl_Test.hndl_DB, hndl_Data, hndl_Trns)
	hndl_Trns = EMF_Transformation_Handle('Past_Lvl_NormRd',trnsKwargs)
	hndl_Word_Acc = EMF_WordSeries_Handle(hndl_Test.hndl_DB, hndl_Data, hndl_Trns)
	plot_data_series(hndl_Data, hndl_Word_Chng, hndl_Word_Acc)

if __name__ == '__main__':
	main()