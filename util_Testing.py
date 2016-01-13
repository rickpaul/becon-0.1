
# EMF 		From...Import
from util_EMF import dt_epoch_to_datetime, dt_add_months, dt_end_of_month, strftime
# System 	Import...As
import numpy as np

def create_test_data_2d_corner(n=1000):
	#Create Test Data: defined on a 3x3 square comprising (0,3) and (0,3)
	x = np.random.random_sample((n,2))*3
	y = np.reshape(
			np.logical_and(x[:,0] > 2,x[:,1] > 1),
		(n,1))
	data = np.hstack((x,y))
	names = ['X0','X1','y']
	dt = np.arange(n)
	categorical = [False, False, True]
	return {'dt': dt, 'data': data, 'names': names, 'categorical': categorical, 'responseIdx': 2}

def create_test_data_2d_cross(n=1000):
	x = np.random.random_sample((n,2))*3
	y = np.reshape(
	        np.logical_or(
	            np.logical_and(x[:,0]>1,x[:,0]<2),
	            np.logical_and(x[:,1]>1,x[:,1]<2)),
	    (n,1))
	data = np.hstack((x,y))
	names = ['X0','X1','y']
	dt = np.arange(n)
	categorical = [False, False, True]
	return {'dt': dt, 'data': data, 'names': names, 'categorical': categorical, 'responseIdx': 2}

def create_test_data_2d_circle(n=1000):
	x = np.random.random_sample((n,2))*3
	y = np.reshape(
			(((x[:,0]-1.5)**2 + (x[:,1]-1.5)**2)<1),
		(n,1))
	data = np.hstack((x,y))
	names = ['X0','X1','y']
	dt = np.arange(n)
	categorical = [False, False, True]
	return {'dt': dt, 'data': data, 'names': names, 'categorical': categorical, 'responseIdx': 2}

def create_test_data_blobs(numDims=4):
	from sklearn.datasets import make_blobs
	n = 20*numDims
	x, y = make_blobs(n_samples=n, n_features=numDims, centers=2*numDims)
	data = np.hstack((x,y.reshape(n,1)))
	names = ['X'+str(i) for i in xrange(numDims)]
	names += ['clusterNum']
	dt = np.arange(n)
	categorical = [False]*numDims
	categorical += [True]
	return {'dt': dt, 'data': data, 'names': names, 'categorical': categorical,  'responseIdx': numDims}


def create_test_data_correlated_returns(n=500, numDims=5, includeResponse=True):
	w = numDims + int(includeResponse)
	returnRange = 1/20.0
	minReturn = 0.0
	#assets have between 0% and 30% std p.a.
	stdRange = 1/4.0
	minStd = 0.05
	#assets have between 0.2 and 0.7 correlation
	corrRange = 1/2.0
	minCorr = 0.2

	mean = (1+np.random.random((w))*returnRange+minReturn)**(1/12.0)-1
	std = (np.random.random((w,1))*stdRange + minStd)/(12.0**.5)
	correl = np.random.random((w,w))*corrRange+minCorr
	correl[range(w),range(w)]=1
	upper = np.triu_indices(w,1)
	lower = (upper[1],upper[0])
	correl[upper] = correl[lower]
	cov = (std * std.T)	* correl

	#Can do Cholesky decomposition method, or...
	data = np.random.multivariate_normal(mean, cov ,size=(n))
	data = data + (np.repeat(np.random.multivariate_normal(mean, cov,size=(n/2+1)),2,0)/2)[:n]
	data = data + (np.repeat(np.random.multivariate_normal(mean, cov,size=(n/4+1)),4,0)/4)[:n]
	data = data + (np.repeat(np.random.multivariate_normal(mean, cov,size=(n/8+1)),8,0)/8)[:n]

	names = ['X'+str(i) for i in xrange(numDims)]
	if includeResponse:
		names += ['y']
		responseIdx = numDims
	else:
		responseIdx = None
	data = np.cumsum(data,0)
	dt = np.arange(n)
	categorical = [False]*w
	return {'dt': dt, 'data': data, 'names': names, 'categorical': categorical,  'responseIdx': responseIdx}

def create_monthly_date_range(n=500, startEpoch=0, asString=True):
	'''sloppy'''
	dt = []
	if asString:
		outputFn = lambda d: strftime(d, '%Y-%m-%d')
	else: #asEpoch
		outputFn = dt_datetime_to_epoch
	currentDT = dt_end_of_month(dt_epoch_to_datetime(startEpoch))
	dt.append(outputFn(currentDT))
	for i in xrange(1,n):
		currentDT = dt_add_months(currentDT, 1)
		dt.append(outputFn(currentDT))
	return dt

def save_test_data_fn(hndl_Test, fn, **kwargs):
	return save_test_data(hndl_Test, **fn(**kwargs))

def save_test_data(hndl_Test, dt, data, names, categorical, responseIdx=None):
	hndl_Test.insert_test_data(dt, data, names, categorical=categorical)
	return (names, responseIdx)

def plot_data_series(*handles):
	from matplotlib import pyplot as plt
	plt.figure(1)
	for hndl in handles:
		plt.plot(hndl.get_series_dates(), hndl.get_series_values())
	plt.show()

if __name__ == '__main__':
	from json import dumps
	from math import sqrt
	from util_EMF import dt_str_YYYY_MM_DD_to_epoch
	series = create_test_data_correlated_returns(n=300, numDims=1, includeResponse=False)
	dt = create_monthly_date_range(n=len(series['dt']))
	json_data = [{'dt':d,'value':v} for (d,v) in zip(dt, series['data'][:,0].tolist())]
	end_val = series['data'][-1,0]
	end_dt = dt_str_YYYY_MM_DD_to_epoch(dt[-1])
	dt_arr = create_monthly_date_range(n=13, startEpoch=end_dt)
	std = np.std(series['data'])
	models = []
	for m in xrange(40):
		d = {	'model_id': str(m),
				'confidence': np.random.random(),
				'model_desc': 'model desc ' + str(m)}
		data = []
		for i in [1,3,6,9,12]:
			data.append({
				'dt' : dt_arr[i],
				'value' : end_val + np.random.normal()*std*sqrt(i),
			})
		d['predictions'] = data
		models.append(d)
	writer = open('__website/history.json', 'wb')
	writer.write(dumps(json_data))
	writer.close()

	writer = open('__website/predictions.json', 'wb')
	writer.write(dumps(models))
	writer.close()
# 	create_test_data_blobs()
# 	create_test_data_2d_circle()
# 	create_test_data_2d_cross()
# 	create_test_data_2d_corner()