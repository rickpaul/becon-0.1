from 	handle_Transformation import EMF_Transformation_Handle
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

if __name__ == '__main__':
	testTransformationHandle()