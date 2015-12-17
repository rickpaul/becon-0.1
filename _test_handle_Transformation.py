from handle_Transformation import EMF_Transformation_Handle


def testTransformationHandle():
	import numpy as np
	np.random.seed(10)
	data = np.random.randint(100,size=(200,1))
	trns_handle = EMF_Transformation_Handle()
	assert np.all(trns_handle.transformDataSeries(data) == data)
	trns_handle.setTransformation1(util_Trns.PrimaryTransformations['FirstOrderDifference'])
	assert trns_handle.transformDataSeries(data).shape == (199,1)
	trns_handle.setExtraParameter('periodDelay', 10)
	assert trns_handle.transformDataSeries(data).shape == (190,1)
	trns_handle.setTransformation2(util_Trns.SecondaryTransformations['FirstOrderDifference'])
	assert trns_handle.transformDataSeries(data).shape == (180,1)


if __name__ == '__main__':
	testTransformationHandle()