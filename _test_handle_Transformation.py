from 	handle_TestSeries 		import EMF_TestSeries_Handle
from 	handle_Transformation 	import EMF_Transformation_Handle
# EMF 		Import...As
import 	util_Testing 			as utl_Tst
# System 	Import...As
import 	numpy as np



def testTransformationHandle():
	np.random.seed(10)
	n=200
	data = np.random.randint(100,size=(n,1))
	dt = np.arange(n)
	hndl_Trns = EMF_Transformation_Handle('None')
	assert np.all(hndl_Trns.transform_data(data) == data)
	assert str(hndl_Trns) == 'raw'
	# Test Past
	hndl_Trns = EMF_Transformation_Handle('Past_Lvl')
	hndl_Trns.set_extra_parameter('PeriodDiff', 10)
	assert hndl_Trns.transform_data(data).shape == (190,1)
	assert np.all(hndl_Trns.transform_time(dt) == np.arange(10,n))
	assert str(hndl_Trns) == 'PastLvl.10'
	# Test Future
	hndl_Trns = EMF_Transformation_Handle('Futr_Change')
	hndl_Trns.set_extra_parameter('PeriodDiff', 20)
	assert hndl_Trns.transform_data(data).shape == (180,1)
	assert np.all(hndl_Trns.transform_time(dt) == np.arange(n-20))
	assert str(hndl_Trns) == 'FutrDiff.20'


def testTransformationReversal_None(data, dt):
	hndl_Trns = EMF_Transformation_Handle('None')
	dt_trns = hndl_Trns.transform_time(dt)
	assert np.all(dt_trns == dt)
	assert np.all(hndl_Trns.reverse_transform_time(dt_trns) == dt)

def testTransformationReversal_Past_Lvl(data, dt, hndl_Srs_Original):
	trnsKwargs={'PeriodDiff': 10}
	hndl_Trns = EMF_Transformation_Handle('Past_Lvl', trnsKwargs=trnsKwargs)
	dt_trns = hndl_Trns.transform_time(dt)
	data_trns = hndl_Trns.transform_data(data)
	hndl_Srs_Trns = EMF_TestSeries_Handle()
	hndl_Srs_Trns.set_series_dates(dt_trns)
	hndl_Srs_Trns.set_series_values(data_trns)
	# utl_Tst.plot_data_series(hndl_Srs_Original, hndl_Srs_Trns)
	assert np.all(dt_trns == dt[10:])
	dt_rvrs = hndl_Trns.reverse_transform_time(dt_trns)
	data_rvrs = hndl_Trns.reverse_transform_data(data_trns)
	hndl_Srs_Rvrs = EMF_TestSeries_Handle()
	hndl_Srs_Rvrs.set_series_dates(dt_rvrs)
	hndl_Srs_Rvrs.set_series_values(data_rvrs)
	utl_Tst.plot_data_series(hndl_Srs_Original, hndl_Srs_Rvrs)
	assert np.all(dt_rvrs == dt[:-10])
	assert np.all(data_rvrs == data[:-10])

def testTransformationReversal_Past_FoD(data, dt, hndl_Srs_Original):
	trnsKwargs={'PeriodDiff': 10}
	hndl_Trns = EMF_Transformation_Handle('Past_Change', trnsKwargs=trnsKwargs)
	dt_trns = hndl_Trns.transform_time(dt)
	data_trns = hndl_Trns.transform_data(data)
	hndl_Srs_Trns = EMF_TestSeries_Handle()
	hndl_Srs_Trns.set_series_dates(dt_trns)
	hndl_Srs_Trns.set_series_values(data_trns)
	# utl_Tst.plot_data_series(hndl_Srs_Original, hndl_Srs_Trns)
	assert np.all(dt_trns == dt[10:])
	assert data_trns[0] == data[10] - data[0]
	dt_rvrs = hndl_Trns.reverse_transform_time(dt_trns)
	data_rvrs = hndl_Trns.reverse_transform_data(data[10:], predictionDelta=data_trns)
	hndl_Srs_Rvrs = EMF_TestSeries_Handle()
	hndl_Srs_Rvrs.set_series_dates(dt_rvrs)
	hndl_Srs_Rvrs.set_series_values(data_rvrs)
	utl_Tst.plot_data_series(hndl_Srs_Original, hndl_Srs_Rvrs)
	assert np.all(dt_rvrs == dt[:-10])
	# assert np.all(data_rvrs == data[:-10])

def testTransformationReversal_Future_FoD(data, dt, hndl_Srs_Original):
	trnsKwargs={'PeriodDiff': 10}
	hndl_Trns = EMF_Transformation_Handle('Futr_Change', trnsKwargs=trnsKwargs)
	dt_trns = hndl_Trns.transform_time(dt)
	data_trns = hndl_Trns.transform_data(data)
	hndl_Srs_Trns = EMF_TestSeries_Handle()
	hndl_Srs_Trns.set_series_dates(dt_trns)
	hndl_Srs_Trns.set_series_values(data_trns)
	# utl_Tst.plot_data_series(hndl_Srs_Original, hndl_Srs_Trns)
	assert np.all(dt_trns == dt[:-10])
	assert data_trns[0] == data[10] - data[00]
	dt_rvrs = hndl_Trns.reverse_transform_time(dt_trns)
	data_rvrs = hndl_Trns.reverse_transform_data(data[:-10], predictionDelta=data_trns)
	hndl_Srs_Rvrs = EMF_TestSeries_Handle()
	hndl_Srs_Rvrs.set_series_dates(dt_rvrs)
	hndl_Srs_Rvrs.set_series_values(data_rvrs)
	utl_Tst.plot_data_series(hndl_Srs_Original, hndl_Srs_Rvrs)
	assert np.all(dt_rvrs == dt[10:])
	# assert np.all(data_rvrs == data[10:])

def testTransformationReversals():
	testInfo = utl_Tst.create_test_data_correlated_returns(numDims=1, n=100)
	data = testInfo['data'][:,0]
	dt = testInfo['dt']
	hndl_Srs_Original = EMF_TestSeries_Handle()
	hndl_Srs_Original.set_series_dates(dt)
	hndl_Srs_Original.set_series_values(data)
	# utl_Tst.plot_data_series(hndl_Srs_Original)
	# testTransformationReversal_None(data, dt)
	# testTransformationReversal_Past_Lvl(data, dt, hndl_Srs_Original)
	testTransformationReversal_Past_FoD(data, dt, hndl_Srs_Original)
	testTransformationReversal_Future_FoD(data, dt, hndl_Srs_Original)

if __name__ == '__main__':
	testTransformationHandle()
	testTransformationReversals()