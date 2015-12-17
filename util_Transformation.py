'''
TODOS:
	+ How do you find quantiles numpy?
'''
import numpy as np
from math import log, e

kwargDefaults = {
	'periodDelay': 1, # 'FirstOrderDifference'
	'numQuartiles': 10, # 'uniformCountRange': 
	'numRanges': 10, # 'uniformLengthRange': 
	'base': e, # 'Logarithm'
}

func_round = np.vectorize(round)
func_abs = np.vectorize(abs)
func_log = np.vectorize(log)

def transform_None(data, kwargs):
	return data

def transform_FirstOrderDifference(data, kwargs):
	key = 'periodDelay'
	periodDelay = kwargs.get(key, kwargDefaults[key])
	return data[periodDelay:] - data[:-periodDelay]

def transform_NormalDistributionZScore(data, kwargs):
	mean = np.mean(data)
	stds = np.std(data)
	return (data - mean)/stds	

def transform_Logarithm(data, kwargs):
	'''
	returns logarithm of data
	'''
	key = 'base'
	base = kwargs.get(key, kwargDefaults[key])
	return func_log(data)/log(base)

def transform_AbsoluteValue(data, kwargs):
	'''
	returns logarithm of data
	'''
	return func_abs(data)

def transform_GrowOutliers(data, kwargs):
	'''
	does a hyperbolic transformation on data centered around median
	'''
	mean = np.mean(data)
	raise NotImplementedError

def transform_ShrinkOutliers(data, kwargs):
	'''
	does an inverse hyperbolic transformation on data centered around median
	'''
	mean = np.mean(data)
	raise NotImplementedError

def categorize_None(data, kwargs):
	'''
	returns sign of data
	'''
	return data

def categorize_Sign(data, kwargs):
	'''
	returns sign of data
	'''
	return np.sign(data)

def categorize_Round(data, kwargs):
	'''
	returns data, categorized to integer ranges by rounding
	(e.g. all data points -.5 to +.5 are categorized as 0)
	(e.g. all data points 1.5 to 2.5 are categorized as 2)
	'''
	return func_round(data)

def categorize_Floor(data, kwargs):
	'''
	returns data, categorized to integer ranges by rounding towards 0
	(e.g. all data points -1 to 1 are categorized as 0)
	(e.g. all data points 1 to 2 are categorized as 1)	
	'''
	return func_round(data - 0.5*np.sign(data))

def categorize_Ceiling(data, kwargs):
	'''
	returns data, categorized to integer ranges by rounding towards 0
	(e.g. all data points 0 to -1 are categorized as -1)
	(e.g. all data points 1 to 2 are categorized as 2)	
	'''
	return func_round(data + 0.5*np.sign(data))

def categorize_UniformLengthRange(data, kwargs):
	'''
	splits data into uniform ranges with non-uniform populations 
	based on overall range of dataset

	TODOS:
	Seems inefficient. Can we do this better?
	'''
	key = 'numRanges'
	numRanges = kwargs.get(key, kwargDefaults[key])
	out = np.zeros(data.shape)
	splits = np.linspace(min(data), max(data), numRanges+1)
	for split in splits[1:]:
		out += data>split
	return out


def categorize_QuantileRange(data, kwargs):
	'''
	returns quantile data
	'''
	key = 'numQuartiles'
	numQuartiles = kwargs.get(key, kwargDefaults[key])
	raise NotImplementedError

def timeSeriesTransform_Trailing(timeSeries, kwargs):
	key = 'periodDelay'
	periodDelay = kwargs.get(key, kwargDefaults[key])
	return timeSeries[periodDelay:]

def timeSeriesTransform_None(timeSeries, kwargs):
	return timeSeries