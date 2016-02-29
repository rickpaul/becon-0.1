# EMF 		From...Import
from 	handle_TestSeries 		import EMF_TestSeries_Handle
from 	handle_TimeSet		 	import EMF_TimeSet_Handle
from 	handle_Transformation 	import EMF_Transformation_Handle
from 	lib_TimeSet 			import DAYS, WEEKS, MONTHS, QUARTERS, YEARS, SECONDS
from 	util_Transformation 	import FIRST_ORDER_DIFF_TIME, PERIODS_AWAY, NUM_RANGES
# EMF 		Import...As
import 	util_Testing 			as utl_Tst
# System 	From...Import
import 	numpy 					as np

dt = np.arange(1,101)
Past_Truncate_dt = np.arange(11,101)
Futr_Truncate_dt = np.arange(1,91)
FoD_Constant = np.ones(shape=(90,))*10
Past_Shift_dt = np.arange(-9,91)
Futr_Shift_dt = np.arange(11,111)


def test_None_pattern(data, hndl_Time):
	hndl_Trns = EMF_Transformation_Handle('None')
	trns_data = hndl_Trns.transform_data(data)
	hndl_Trns.transform_time(hndl_Time)
	assert np.all(trns_data == data)
	assert np.all(hndl_Time.get_dates() == dt)
	trns_data = hndl_Trns.reverse_transform_data(None, modifier=data)
	hndl_Trns.reverse_transform_time(hndl_Time)
	assert np.all(trns_data == data)
	assert np.all(hndl_Time.get_dates() == dt)

def test_Past_Change_pattern(data, hndl_Time):
	trns_kwargs = {FIRST_ORDER_DIFF_TIME:10}
	hndl_Trns = EMF_Transformation_Handle('Past_Change', trnsKwargs=trns_kwargs)
	trns_data = hndl_Trns.transform_data(data)
	hndl_Trns.transform_time(hndl_Time)
	assert np.all(trns_data == FoD_Constant)
	assert np.all(hndl_Time.get_dates() == Past_Truncate_dt)
	trns_data = hndl_Trns.reverse_transform_data(data[10:], modifier=trns_data)
	hndl_Trns.reverse_transform_time(hndl_Time)
	assert np.all(trns_data == data[0:-10])
	assert np.all(hndl_Time.get_dates() == dt[0:-10])

def test_Futr_Change_pattern(data, hndl_Time):
	trns_kwargs = {FIRST_ORDER_DIFF_TIME:10}
	hndl_Trns = EMF_Transformation_Handle('Futr_Change', trnsKwargs=trns_kwargs)
	trns_data = hndl_Trns.transform_data(data)
	hndl_Trns.transform_time(hndl_Time)
	assert np.all(trns_data == FoD_Constant)
	assert np.all(hndl_Time.get_dates() == Futr_Truncate_dt)
	trns_data = hndl_Trns.reverse_transform_data(data[:-10], modifier=trns_data)
	hndl_Trns.reverse_transform_time(hndl_Time)
	assert np.all(trns_data == data[10:])
	assert np.all(hndl_Time.get_dates() == dt[10:])

def test_Futr_Level_pattern(data, hndl_Time):
	trns_kwargs = {PERIODS_AWAY:10}
	hndl_Trns = EMF_Transformation_Handle('Futr_Lvl', trnsKwargs=trns_kwargs)
	trns_data = hndl_Trns.transform_data(data)
	hndl_Trns.transform_time(hndl_Time)
	assert np.all(trns_data == data)
	assert np.all(hndl_Time.get_dates() == Past_Shift_dt)
	trns_data = hndl_Trns.reverse_transform_data(None, modifier=trns_data)
	hndl_Trns.reverse_transform_time(hndl_Time)
	assert np.all(trns_data == data)
	assert np.all(hndl_Time.get_dates() == dt)

def test_Past_Level_pattern(data, hndl_Time):
	trns_kwargs = {PERIODS_AWAY:10}
	hndl_Trns = EMF_Transformation_Handle('Past_Lvl', trnsKwargs=trns_kwargs)
	trns_data = hndl_Trns.transform_data(data)
	hndl_Trns.transform_time(hndl_Time)
	assert np.all(trns_data == data)
	assert np.all(hndl_Time.get_dates() == Futr_Shift_dt)
	trns_data = hndl_Trns.reverse_transform_data(None, modifier=trns_data)
	hndl_Trns.reverse_transform_time(hndl_Time)
	assert np.all(trns_data == data)
	assert np.all(hndl_Time.get_dates() == dt)

def test_Current_Level_Cat_pattern(data, hndl_Time):
	hndl_Srs = EMF_TestSeries_Handle()
	hndl_Srs.values = data
	hndl_Srs.dates = hndl_Time.get_dates()
	trns_kwargs = {NUM_RANGES:10, FIRST_ORDER_DIFF_TIME:10}
	hndl_Trns = EMF_Transformation_Handle('Futr_Lvl_Cat', trnsKwargs=trns_kwargs)
	trns_data = hndl_Trns.transform_data(data)
	hndl_Trns.transform_time(hndl_Time)

	hndl_Srs_Trns = EMF_TestSeries_Handle()
	hndl_Srs_Trns.values = trns_data
	hndl_Srs_Trns.dates = hndl_Time.get_dates()
	utl_Tst.plot_data_series(hndl_Srs, hndl_Srs_Trns)

	raise NotImplementedError

	# assert np.all(trns_data == data)
	# assert np.all(hndl_Time.get_dates() == dt)
	# trns_data = hndl_Trns.reverse_transform_data(None, modifier=trns_data)
	# hndl_Trns.reverse_transform_time(hndl_Time)
	# assert np.all(trns_data == data)
	# assert np.all(hndl_Time.get_dates() == dt)

def get_test_TimeHandle():
	hndl_Time = EMF_TimeSet_Handle()
	hndl_Time.periodicity = SECONDS
	hndl_Time.startEpoch = 1
	hndl_Time.endEpoch = 100
	return hndl_Time

def main():
	data = utl_Tst.create_test_data_linear_change(n=100, increase=1)['data']
	hndl_Time = get_test_TimeHandle()
	test_None_pattern(data, hndl_Time)
	hndl_Time = get_test_TimeHandle()
	test_Past_Change_pattern(data, hndl_Time)
	hndl_Time = get_test_TimeHandle()
	test_Futr_Level_pattern(data, hndl_Time)
	hndl_Time = get_test_TimeHandle()
	test_Past_Level_pattern(data, hndl_Time)
	data = utl_Tst.create_test_data_correlated_returns(numDims=1, n=100)['data'][:,0]
	hndl_Time = get_test_TimeHandle()
	test_Current_Level_Cat_pattern(data, hndl_Time)


if __name__ == '__main__':
	main()