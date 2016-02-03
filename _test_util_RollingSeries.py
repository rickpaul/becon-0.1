
from util_RollingStats 	import NonSequentialRegressionWindow, SequentialRegressionWindow, RollingMeanVarianceWindow
from util_Testing 		import create_test_data_correlated_returns

import numpy as np
from scipy import stats

def testNonSequentialRegression(errorLimit=1e-11,verbose=True):
	print '*************************************',
	print 'TESTING NON SEQUENTIAL REGRESSION'
	numDims=2
	n=480
	data = create_test_data_correlated_returns(n=n, numDims=numDims, includeResponse=False)
	dataX = data['data'][:,0]
	dataY = data['data'][:,1]

	# Create Regression Window
	windowSize = 100
	RW = NonSequentialRegressionWindow(dataX,dataY,windowSize)

	spots = np.random.randint(n-windowSize,size=(10))
	for spot in spots:
		x = dataX[spot:spot+windowSize]
		y = dataY[spot:spot+windowSize]
		(slope, intercept, r_value, p_value, std_err) = stats.linregress(x,y)
		createdSlope = RW.slopes[spot]
		createdIntercept = RW.intercepts[spot]
		print '*************************************',
		print spot
		if verbose:
			print 'Slope:',
			print slope, 
			print createdSlope,
			print slope - createdSlope
			# print '*************'
			print 'Intercept:',
			print intercept, 
			print createdIntercept,
			print intercept - createdIntercept
		print ('OK!' if (abs(slope - createdSlope) < errorLimit) and (abs(intercept - createdIntercept) < errorLimit) else 'Failed')



def testSequentialRegression(errorLimit=1e-11,verbose=True):
	print '*************************************',
	print 'TESTING SEQUENTIAL REGRESSION'
	numDims=2
	n=480
	data = create_test_data_correlated_returns(n=n, numDims=numDims, includeResponse=False)
	dataY = data['data'][:,1]

	# Create Regression Window
	windowSize = 100
	RW = SequentialRegressionWindow(dataY,windowSize)

	spots = np.random.randint(n-windowSize,size=(10))
	for spot in spots:
		x = np.arange(0,windowSize)
		y = dataY[spot:spot+windowSize]
		(slope, intercept, r_value, p_value, std_err) = stats.linregress(x,y)
		createdSlope = RW.slopes[spot]
		createdIntercept = RW.intercepts[spot]
		print '*************************************',
		print spot
		if verbose:
			print 'Slope:',
			print slope, 
			print createdSlope,
			print slope - createdSlope
			# print '*************'
			print 'Intercept:',
			print intercept, 
			print createdIntercept,
			print intercept - createdIntercept
		print ('OK!' if (abs(slope - createdSlope) < errorLimit) and (abs(intercept - createdIntercept) < errorLimit) else 'Failed')



def testMeanVariance(errorLimit=1e-11,verbose=True):
	print '*************************************',
	print 'TESTING MEAN VARIANCE'
	numDims=2
	n=480
	data = create_test_data_correlated_returns(n=n, numDims=numDims, includeResponse=False)
	dataY = data['data'][:,1]

	# Create Regression Window
	windowSize = 100
	RW = RollingMeanVarianceWindow(dataY,windowSize)

	spots = np.random.randint(n-windowSize,size=(10))
	for spot in spots:
		y = dataY[spot:spot+windowSize]
		mean = np.mean(y)
		variance = np.var(y)
		createdMean = RW.means[spot]
		createdVariance = RW.variances[spot]
		print '*************************************',
		print spot
		if verbose:
			print 'Mean:',
			print mean, 
			print createdMean,
			print mean - createdMean
			# print '*************'
			print 'Variance:',
			print variance, 
			print createdVariance,
			print variance - createdVariance
		print ('OK!' if (abs(mean - createdMean) < errorLimit) and (abs(variance - createdVariance) < errorLimit) else 'Failed')


if __name__ == '__main__':
	verbose = 1
	# testSequentialRegression(verbose=verbose)
	# testNonSequentialRegression(verbose=verbose)
	testMeanVariance(verbose=verbose)

