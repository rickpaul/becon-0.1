# System 	Import...As
import numpy as np

def createTestData_2D_Corner(n=1000):
	#Create Test Data: defined on a 3x3 square comprising (0,3) and (0,3)
	x = np.random.random_sample((n,2))*3
	y = np.reshape(
			np.logical_and(x[:,0] > 2,x[:,1] > 1),
		(n,1))
	return {'dataset': np.hstack((x,y)), 'names': ['x1','x2','y']}

def createTestData_2D_Cross(n=1000):
	x = np.random.random_sample((n,2))*3
	y = np.reshape(
	        np.logical_or(
	            np.logical_and(x[:,0]>1,x[:,0]<2),
	            np.logical_and(x[:,1]>1,x[:,1]<2)),
	    (n,1))
	return {'dataset': np.hstack((x,y)), 'names': ['x1','x2','y']}

def createTestData_2D_Circle(n=1000):
	x = np.random.random_sample((n,2))*3
	y = np.reshape(
			(((x[:,0]-1.5)**2 + (x[:,1]-1.5)**2)<1),
		(n,1))
	return {'dataset': np.hstack((x,y)), 'names': ['x1','x2','y']}

def save_test_data_blobs(hndl_Test, numDims=4):
	from sklearn.datasets import make_blobs
	dataLen = 20*numDims
	X, y = make_blobs(n_samples=dataLen, n_features=numDims, centers=2*numDims)
	dt = np.arange(dataLen)
	dataNames = ['X'+str(i) for i in xrange(numDims)]
	hndl_Test.insert_test_data(dt, X, dataNames, categorical=False)
	hndl_Test.insert_test_data(dt, y, ['clusterNum'], categorical=True)
	return (dataNames, ['clusterNum'])


