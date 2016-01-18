# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Testing 			import EMF_Testing_Handle
from 	handle_Transformation	import EMF_Transformation_Handle
from 	handle_WordSeries		import EMF_WordSeries_Handle
from 	runner_Model 			import EMF_Model_Runner
from 	lib_EMF 				import TEMP_MODE
from 	util_Testing 			import save_test_data_fn, create_test_data_linear_change
from 	util_Testing 			import plot_data_series

def main():
	hndl_Test = EMF_Testing_Handle(mode=TEMP_MODE)
	fn = create_test_data_linear_change
	(tickers, responseIdx) = save_test_data_fn(hndl_Test, fn, n=100)
	hndl_Data = EMF_DataSeries_Handle(hndl_Test.hndl_DB, ticker=tickers[0])
	# hndl_Trns = EMF_Transformation_Handle('RateOfChange')
	# hndl_Trns.set_extra_parameter('PeriodDiff', 12)
	# hndl_Word = EMF_WordSeries_Handle(hndl_Test.hndl_DB, hndl_Data, hndl_Trns)
	# plot_data_series(hndl_Data, hndl_Word)
	# hndl_Trns = EMF_Transformation_Handle('RateOfChange_Cat')
	# hndl_Trns.set_extra_parameter('PeriodDiff', 12)
	# hndl_Word = EMF_WordSeries_Handle(hndl_Test.hndl_DB, hndl_Data, hndl_Trns)
	# plot_data_series(hndl_Data, hndl_Word)
	trnsKwargs = {'PeriodDiff': 10}
	hndl_Trns = EMF_Transformation_Handle('Futr_Lvl', trnsKwargs)
	hndl_Word_Chng = EMF_WordSeries_Handle(hndl_Test.hndl_DB, hndl_Data, hndl_Trns)
	# hndl_Trns = EMF_Transformation_Handle('Past_Lvl_NormRd',trnsKwargs)
	# hndl_Word_Acc = EMF_WordSeries_Handle(hndl_Test.hndl_DB, hndl_Data, hndl_Trns)
	plot_data_series(hndl_Data, hndl_Word_Chng)

if __name__ == '__main__':
	main()