# TODO:
#	Make transformations return metadata
# System 	Import...As
import 	numpy 		as np
import 	logging 	as log
# System 	From...Import
from 	math 		import log as log_
from 	math 		import e

kwargDefaults = {
	'PeriodDiff': 1,
	'numQuartiles': 10, # 'uniformCountRange': 
	'numRanges': 10, # 'uniformLengthRange': 
	'base': e, # 'Logarithm'
	'value': 1,
	'power': 1.5, # power >= 1!
}

func_round = np.vectorize(round)
func_abs = np.vectorize(abs)
func_log = np.vectorize(log_)

# DATA VERIFICATIONS

def verify_None(data, kwargs):
	return True

def verify_Positive(data, kwargs):
	return np.all(data>0)

# DATA TRANSFORMATIONS

def transform_None(data, kwargs):
	return data

def transform_usePredictions(data, predictions, kwargs):
	return predictions

def transform_FOD_BackwardLooking(data, kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return data[periodDelta:] - data[:-periodDelta]

def transform_FOD_ForwardLooking(data, kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return data[periodDelta:] - data[:-periodDelta]

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
	return func_log(data)/log_(base)

def transform_AbsoluteValue(data, kwargs):
	'''
	returns logarithm of data
	'''
	return func_abs(data)

def transform_GrowOutliers(data, kwargs):
	'''
	does a power (power >= 1!) transformation on the data (data >= 1!)
	TODO:
			Re-implement to tanh
	'''
	key = 'power'
	power = kwargs.get(key, kwargDefaults[key])
	sgn_d = np.sign(data)
	return np.power(data,power)*sgn_d

def transform_ShrinkOutliers(data, kwargs):
	'''
	does an inverse power (power >= 1!) transformation on the data (data >= 1!)
	TODO:
			Re-implement to tanh
	'''
	key = 'power'
	power = kwargs.get(key, kwargDefaults[key])
	sgn_d = np.sign(data)
	return np.power(data,1/power)*sgn_d

def transform_AddSeries(baseSeries, addSeries, kwargs):
	return baseSeries + addSeries

def transform_SubtractSeries(baseSeries, subSeries, kwargs):
	return baseSeries - subSeries

def transform_TimeToValue(data, kwargs):
	key = 'value'
	value = kwargs.get(key, kwargDefaults[key])
	out = np.ones(data.shape)*-1
	len_ = len(data)
	counter = 0
	for i in xrange(len_):
		if data[i]==value:
			for j in xrange(1,counter+1):
				out[i-j] = j
			out[i] = 0
			counter = 0
		else:
			counter += 1
	return out

def transform_TimeSinceValue(data, kwargs):
	key = 'value'
	value = kwargs.get(key, kwargDefaults[key])
	out = np.ones(data.shape)*-1
	len_ = len(data)
	record = False
	counter = 0
	for i in xrange(len_):
		if data[i]==value:
			out[i] = 0
			counter = 0
			record = 1
		else:
			if record:
				out[i] = counter+1
			counter += 1
	return out

# CATEGORIZATIONS

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

def categorize_MoreThanAmount(data, kwargs):
	raise NotImplementedError

def categorize_LessThanAmount(data, kwargs):
	raise NotImplementedError

# TIME SERIES TRANSFORMATIONS
# def timeSeriesTransform_TruncateUntilValue(timeSeries, dataSeries, kwargs):
# 	'''
# 	TODO:
# 				Modify time series transformations to take data *and* times
# 	'''
# 	raise NotImplementedError
# 	key = 'value'
# 	value = kwargs.get(key, kwargDefaults[key])


def timeSeriesTransform_TruncatePast(timeHandle, kwargs):
	key = 'PeriodDiff'
	delta = kwargs.get(key, kwargDefaults[key])
	timeHandle.truncate_start(delta)

def timeSeriesTransform_TruncateFuture(timeHandle, kwargs):
	key = 'PeriodDiff'
	delta = kwargs.get(key, kwargDefaults[key])
	timeHandle.truncate_end(delta)

def timeSeriesTransform_ShiftFuture(timeHandle, kwargs):
	key = 'PeriodDiff'
	delta = kwargs.get(key, kwargDefaults[key])
	timeHandle.shift_forward(delta)

def timeSeriesTransform_ShiftPast(timeHandle, kwargs):
	key = 'PeriodDiff'
	delta = kwargs.get(key, kwargDefaults[key])
	timeHandle.shift_backward(delta)

def timeSeriesTransform_None(timeHandle, kwargs):
	pass

# TRANSFORMATION PATTERNS NAMES

def transformStr_None(kwargs):
	return 'raw'

def transformStr_Cat(kwargs):
	key = 'numRanges'
	numCats = kwargs.get(key, kwargDefaults[key])	
	return 'raw->Cat.{0}'.format(numCats)

def transformStr_NormRd(kwargs):
	return 'raw->NormRd'

def transformStr_PastDiff(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'PastDiff.{0}'.format(periodDelta)

def transformStr_PastDiffCat(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	key = 'numRanges'
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'PastDiff.{0}->Cat.{1}'.format(periodDelta, numCats)

def transformStr_PastDiffNormRd(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'PastDiff.{0}->NormRd'.format(periodDelta)

def transformStr_PastLvl(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'PastLvl.{0}'.format(periodDelta)

def transformStr_PastLvlCat(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	key = 'numRanges'
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'PastLvl.{0}->Cat.{1}'.format(periodDelta, numCats)

def transformStr_PastLvlNormRd(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'PastLvl.{0}->NormRd'.format(periodDelta)

def transformStr_FutrLvl(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'FutrLvl.{0}'.format(periodDelta)

def transformStr_FutrLvlCat(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	key = 'numRanges'
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'FutrLvl.{0}->Cat.{1}'.format(periodDelta, numCats)

def transformStr_FutrLvlNormRd(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'FutrLvl.{0}->NormRd'.format(periodDelta)

def transformStr_FutrDiff(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'FutrDiff.{0}'.format(periodDelta)

def transformStr_FutrDiffCat(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	key = 'numRanges'
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'FutrDiff.{0}->Cat.{1}'.format(periodDelta, numCats)

def transformStr_FutrDiffNormRd(kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'FutrDiff.{0}->NormRd'.format(periodDelta)


# if __name__ == '__main__':
# 	len_ = 11
# 	x = np.random.randint(9, size=(len_))+1
# 	d = np.zeros((x[0],1))
# 	for i in xrange(1,len_):
# 	    if i%2==0:
# 	        d = np.vstack((d,np.zeros((x[i],1))))
# 	    else:
# 	        d = np.vstack((d,np.ones((x[i],1))))

# 	d = d.ravel()
# 	len_ = len(d)
# 	print np.hstack((transform_TimeSinceValue(d, {'value': 1}).reshape(len_,1),
# 					d.reshape(len_,1)))
