# TODO:
#	Make transformations return metadata
# System 	Import...As
import 	numpy 		as np
import 	logging 	as log
# System 	From...Import
from 	math 		import log as log_
from 	math 		import e

DATA_KEY 					= 'D'
SPLITS_KEY 					= 'S'
TIME_TO_VALUE 				= 'TTV_V' 
TIME_SINCE_VALUE 			= 'TSV_V' 
FIRST_ORDER_DIFF_TIME 		= 'FoD_T' 
PERIODS_AWAY				= 'P_T'
NUM_QUARTILES				= 'NQ'
NUM_RANGES					= 'NR'
BASE						= 'b'
POWER						= 'p'
ABOVE_LIMIT					= 'AL'
BELOW_LIMIT					= 'BL'
TRAILING_VOL_TIME			= 'TVol_T'
TRAILING_AVG_TIME			= 'TAvg_T'


kwargDefaults = {
	FIRST_ORDER_DIFF_TIME: 	1,
	PERIODS_AWAY: 			1,
	NUM_QUARTILES: 			10, # 'uniformCountRange': 
	NUM_RANGES: 			10, # 'uniformLengthRange': 
	BASE: 					e, # 'Logarithm'
	TIME_SINCE_VALUE: 		1, # Which value are we seeking?
	TIME_TO_VALUE: 			1, # Which value are we seeking?
	POWER: 					1.5, # power >= 1!
	ABOVE_LIMIT: 			2.0,
	BELOW_LIMIT: 			-2.0,
	TRAILING_VOL_TIME: 		36,
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
	return {DATA_KEY: data,
			}

def transform_usePredictions(data, predictions, kwargs):
	return {DATA_KEY: predictions,
			}

def transform_FOD_BackwardLooking(data, kwargs):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return {DATA_KEY: data[periodDelta:] - data[:-periodDelta],
			}

def transform_FOD_ForwardLooking(data, kwargs):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return {DATA_KEY: data[periodDelta:] - data[:-periodDelta],
			}

def transform_NormalDistributionZScore(data, kwargs):
	mean = np.mean(data)
	stds = np.std(data)
	return {DATA_KEY: (data - mean)/stds,
			}

def transform_Logarithm(data, kwargs):
	'''
	returns logarithm of data
	'''
	key = BASE
	base = kwargs.get(key, kwargDefaults[key])
	return {DATA_KEY: func_log(data)/log_(base),
			}

def transform_AbsoluteValue(data, kwargs):
	'''
	returns logarithm of data
	'''
	return {DATA_KEY: func_abs(data),
			}

def transform_GrowOutliers(data, kwargs):
	'''
	does a power (power >= 1!) transformation on the data (data >= 1!)
	TODO:
			Re-implement to tanh
	'''
	key = POWER
	power = kwargs.get(key, kwargDefaults[key])
	sgn_d = np.sign(data)
	return {DATA_KEY: np.power(data,power)*sgn_d,
			}

def transform_ShrinkOutliers(data, kwargs):
	'''
	does an inverse power (power >= 1!) transformation on the data (data >= 1!)
	TODO:
			Re-implement to tanh
	'''
	key = POWER
	power = kwargs.get(key, kwargDefaults[key])
	sgn_d = np.sign(data)
	return {DATA_KEY: np.power(data,1/power)*sgn_d,
			}

def transform_AddSeries(baseSeries, addSeries, kwargs):
	return {DATA_KEY: baseSeries + addSeries,
			}

def transform_SubtractSeries(baseSeries, subSeries, kwargs):
	return {DATA_KEY: baseSeries - subSeries,
			}

def transform_TimeToValue(data, kwargs):
	key = TIME_TO_VALUE
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
	return {DATA_KEY: out,
			}

def transform_TimeSinceValue(data, kwargs):
	key = TIME_SINCE_VALUE
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
	return {DATA_KEY: out,
			}

def transform_TrailingVolatility(data, kwargs):
	key = TRAILING_VOL_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	raise NotImplementedError

def transform_SimpleTrailingMovingAverage(data, kwargs):
	'''
	np.convolve applies linear convolution of 2 1-D signals
		Convolution is complicated. See wiki.
		http://en.wikipedia.org/wiki/Convolution
		'valid' ensures that only sequences with full data are taken.
		'valid' thus includes one more period than you would think. 
			A rolling 50 has data in the 50th cell, not the 51st, 
			as a subsetting[50:] would suggest.
	'''
	key = TRAILING_AVG_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	weights = np.repeat(1.0, periodDelta)/periodDelta
	return {DATA_KEY: np.convolve(data, weights, 'valid'),
			}


def transform_ExponentialTrailingMovingAverage(data, kwargs):
	key = TRAILING_AVG_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	base = np.exp(-np.log(periodDelta)/periodDelta)
	weights = base**np.arange(0, periodDelta)
	weights = weights/sum(weights)
	return {DATA_KEY: np.convolve(data, weights, 'valid'),
			}



# def transform_TrailingMinMaxChannel(data, periodDelta=None):
# 	key = 'PeriodDiff'
# 	periodDelta = kwargs.get(key, kwargDefaults[key])
# 	# Define helper functions for finding min/max functions 
# 	#CONSIDER: We could fold these functions into the lines for a shorter (but less legible) function
# 	def resetMins(values):
# 		min_index, min_value = min(enumerate(values), key=operator.itemgetter(1))
# 		return (min_index, min_value)
# 	def resetMaxs(values):
# 		max_index, max_value = max(enumerate(values), key=operator.itemgetter(1))
# 		return (max_index, max_value)
# 	# Fill in initial min and max values
# 	dataLength = len(dataStream)
# 	minimumChannel = np.zeros(dataLength-periodDelta + 1)
# 	maximumChannel = np.zeros(dataLength-periodDelta + 1)
# 	(max_index, max_value) = resetMaxs(dataStream[0:periodDelta])
# 	(min_index, min_value) = resetMins(dataStream[0:periodDelta])
# 	# Loop Through DataStream
# 	#TODO: Verify indexes are working as thought 
# 	for i  in range(0, len(minimumChannel)):
# 		# Loop Through DataStream / Check maximum trail should end?
# 		if dataStream[periodDelta + i - 1] >= max_value:
# 			max_value = dataStream[periodDelta + i - 1]
# 			max_index = periodDelta
# 		elif max_index <= 0:
# 			(max_index, max_value) = resetMaxs(dataStream[i:i+periodDelta])
# 		# Loop Through DataStream / Check minimum trail should end?
# 		if dataStream[periodDelta + i - 1] <= min_value:
# 			min_value = dataStream[periodDelta + i - 1]
# 			min_index = periodDelta
# 		elif min_index <= 0:
# 			(min_index, min_value) = resetMins(dataStream[i:i+periodDelta])
# 		# Loop Through DataStream / Update Saved Values
# 		minimumChannel[i] = min_value
# 		maximumChannel[i] = max_value
# 		max_index -= 1
# 		min_index -= 1
# 	return (minimumChannel, maximumChannel)


# def PercentBand(movingAvgDataStream, percentBand=None): 
# 	if percentBand is None:
# 		percentBand = 0.05 #default PercentBand is 10%
# 	minimumChannel = movingAvgDataStream * (1 - percentBand)
# 	maximumChannel = movingAvgDataStream * (1 + percentBand)
# 	return (minimumChannel, maximumChannel)		

# def BollingerBand(dataStream, trailPeriod=None, bandwidth=None): 
# 	if trailPeriod is None:
# 		trailPeriod = TRAIL_PERIOD_DEFAULT
# 	if bandwidth is None:
# 		bandwidth = 1.96 #default bandwidth assumes normal dist returns, looks for 10% events
# 	centerLine = ExponentialTrailingMovingAverage(dataStream, trailPeriod=trailPeriod)
# 	dataLength = len(dataStream)
# 	minimumChannel = np.zeros(dataLength-trailPeriod + 1)
# 	maximumChannel = np.zeros(dataLength-trailPeriod + 1)
# 	for i  in range(0, len(minimumChannel)):
# 		sd = np.std(dataStream[i:i+trailPeriod])
# 		minimumChannel[i] = centerLine[i]-bandwidth*sd
# 		maximumChannel[i] = centerLine[i]+bandwidth*sd
# 	return (minimumChannel, maximumChannel)


# CATEGORIZATIONS

def categorize_None(data, kwargs):
	'''
	returns data unchanged
	'''
	return {DATA_KEY: data,}


def categorize_Sign(data, kwargs):
	'''
	returns sign of data
	'''
	return {DATA_KEY: np.sign(data),
			SPLITS_KEY: [0]
			}

def categorize_Round(data, kwargs):
	'''
	returns data, categorized to integer ranges by rounding
	(e.g. all data points -.5 to +.5 are categorized as 0)
	(e.g. all data points 1.5 to 2.5 are categorized as 2)
	'''
	return {DATA_KEY: func_round(data),
			}

def categorize_Floor(data, kwargs):
	'''
	returns data, categorized to integer ranges by rounding towards 0
	(e.g. all data points -1 to 1 are categorized as 0)
	(e.g. all data points 1 to 2 are categorized as 1)	
	'''
	return {DATA_KEY: func_round(data - 0.5*np.sign(data)),
			}

def categorize_Ceiling(data, kwargs):
	'''
	returns data, categorized to integer ranges by rounding towards 0
	(e.g. all data points 0 to -1 are categorized as -1)
	(e.g. all data points 1 to 2 are categorized as 2)	
	'''
	return {DATA_KEY: func_round(data + 0.5*np.sign(data)),
			}

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
	return {DATA_KEY: out,
			}

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
# 	key = TIME_SINCE_VALUE
# 	value = kwargs.get(key, kwargDefaults[key])


def timeSeriesTransform_TruncatePast(timeHandle, kwargs):
	key = FIRST_ORDER_DIFF_TIME
	delta = kwargs.get(key, kwargDefaults[key])
	timeHandle.truncate_start(delta)

def timeSeriesTransform_TruncateFuture(timeHandle, kwargs):
	key = FIRST_ORDER_DIFF_TIME
	delta = kwargs.get(key, kwargDefaults[key])
	timeHandle.truncate_end(delta)

def timeSeriesTransform_ShiftFuture(timeHandle, kwargs):
	key = PERIODS_AWAY
	delta = kwargs.get(key, kwargDefaults[key])
	timeHandle.shift_forward(delta)

def timeSeriesTransform_ShiftPast(timeHandle, kwargs):
	key = PERIODS_AWAY
	delta = kwargs.get(key, kwargDefaults[key])
	timeHandle.shift_backward(delta)

def timeSeriesTransform_None(timeHandle, kwargs):
	pass

# TRANSFORMATION PATTERNS NAMES

def transformStr_None(kwargs):
	return 'raw'

def transformStr_Cat(kwargs):
	key = NUM_RANGES
	numCats = kwargs.get(key, kwargDefaults[key])	
	return 'raw->Cat.{0}'.format(numCats)

def transformStr_NormRd(kwargs):
	return 'raw->NormRd'

def transformStr_PastDiff(kwargs):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'PastDiff.{0}'.format(periodDelta)

def transformStr_PastDiffCat(kwargs):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	key = NUM_RANGES
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'PastDiff.{0}->Cat.{1}'.format(periodDelta, numCats)

def transformStr_PastDiffNormRd(kwargs):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'PastDiff.{0}->NormRd'.format(periodDelta)

def transformStr_PastLvl(kwargs):
	key = PERIODS_AWAY
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'PastLvl.{0}'.format(periodDelta)

def transformStr_PastLvlCat(kwargs):
	key = PERIODS_AWAY
	periodDelta = kwargs.get(key, kwargDefaults[key])
	key = NUM_RANGES
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'PastLvl.{0}->Cat.{1}'.format(periodDelta, numCats)

def transformStr_PastLvlNormRd(kwargs):
	key = PAST_LEVEL
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'PastLvl.{0}->NormRd'.format(periodDelta)

def transformStr_FutrLvl(kwargs):
	key = PERIODS_AWAY
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'FutrLvl.{0}'.format(periodDelta)

def transformStr_FutrLvlCat(kwargs):
	key = PERIODS_AWAY
	periodDelta = kwargs.get(key, kwargDefaults[key])
	key = NUM_RANGES
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'FutrLvl.{0}->Cat.{1}'.format(periodDelta, numCats)

def transformStr_FutrLvlNormRd(kwargs):
	key = PERIODS_AWAY
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'FutrLvl.{0}->NormRd'.format(periodDelta)

def transformStr_FutrDiff(kwargs):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'FutrDiff.{0}'.format(periodDelta)

def transformStr_FutrDiffCat(kwargs):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	key = NUM_RANGES
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'FutrDiff.{0}->Cat.{1}'.format(periodDelta, numCats)

def transformStr_FutrDiffNormRd(kwargs):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'FutrDiff.{0}->NormRd'.format(periodDelta)

def LIST_SPLITS(splits, value):
	try:
		i = next(x[0] for x in enumerate(splits) if x[1] > value)
	except StopIteration:
		limit_above = None
		limit_below = splits[len(splits)-1]
	else:
		if i == 0:
			limit_above = splits[0]
			limit_below = None
		else:
			limit_above = splits[i]
			limit_below = splits[i-1]
	return (limit_above, limit_below)

def LIMITS_STRING(splits, value):
	(limit_above, limit_below) = LIST_SPLITS(splits, value)
	if limit_above is None:
		return 'above {0}'.format(limit_below)
	elif limit_below is None:
		return 'below {0}'.format(limit_above)
	else:
		return 'between {0} and {1}'.format(limit_below, limit_above)

def NORM_ROUND_STRING(value):
	if value > 1:
		return '({0} std. devs above long-term average)'.format(value)
	elif value > 0:
		return '(1 std. dev above long-term average)'
	elif value < -1:
		return '({0} std. devs below long-term average)'.format(value)
	elif value < 0:
		return '(1 std. dev below long-term average)'
	else:
		return '(around long-term average)'

# TRANSFORMATION PATTERNS SPECIFIC Descriptions

def spec_desc_None(kwargs, name, value, splits):
	return 'Value of {0} is {1}'.format(name, value)

def spec_desc_Cat(kwargs, name, value, splits):
	limit_string = LIMITS_STRING(splits, value)
	return 'Value of {0} is {1}'.format(name, limit_string)

def spec_desc_NormRd(kwargs, name, value, splits):
	limit_string = LIMITS_STRING(splits, value)
	norm_round_string = NORM_ROUND_STRING(value)
	return 'Value of {0} is {1} {2}'.format(name, limit_string, norm_round_string)

def spec_desc_PastDiff(kwargs, name, value, splits):
	up_down_string = 'down' if value < 0 else 'up'
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'Value of {0} is {1} {2} since {3} ago.'.format(name, up_down_string, value, periodDelta)

def spec_desc_PastDiffCat(kwargs, name, value, splits):
	up_down_string = 'down' if value < 0 else 'up'
	limit_string = LIMITS_STRING(splits, value)
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'Value of {0} is {1} {2} since {3} ago.'.format(name, up_down_string, limit_string, periodDelta)

def spec_desc_PastDiffNormRd(kwargs, name, value, splits):
	limit_string = LIMITS_STRING(splits, value)
	norm_round_string = NORM_ROUND_STRING(value)
	up_down_string = 'down' if value < 0 else 'up'
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return 'Value of {0} is {1} {2} {3} since {4} ago.'.format(name, up_down_string, limit_string, norm_round_string, periodDelta)

def spec_desc_PastLvl(kwargs, name, value, splits):
	raise NotImplementedError

def spec_desc_PastLvlCat(kwargs, name, value, splits):
	raise NotImplementedError

def spec_desc_PastLvlNormRd(kwargs, name, value, splits):
	raise NotImplementedError

def spec_desc_FutrLvl(kwargs, name, value, splits):
	raise NotImplementedError

def spec_desc_FutrLvlCat(kwargs, name, value, splits):
	raise NotImplementedError

def spec_desc_FutrLvlNormRd(kwargs, name, value, splits):
	raise NotImplementedError
	
def spec_desc_FutrDiff(kwargs, name, value, splits):
	raise NotImplementedError
	
def spec_desc_FutrDiffCat(kwargs, name, value, splits):
	raise NotImplementedError

def spec_desc_FutrDiffNormRd(kwargs, name, value, splits):
	raise NotImplementedError


def gen_desc_None(kwargs, name):
	return 'Value of {0}'.format(name)

def gen_desc_Cat(kwargs, name):
	key = NUM_RANGES
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'Value of {0} in {1} categories'.format(name, numCats)

def gen_desc_NormRd(kwargs, name):
	return 'Number of standard deviations above/below long-term mean of {0}'.format(name)

def gen_desc_PastDiff(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	numPeriods = kwargs.get(key, kwargDefaults[key])
	return 'Change in {0} since {1} periods ago'.format(name, numPeriods)

def gen_desc_PastDiffCat(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	key = NUM_RANGES
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'Change in {0} since {1} periods ago in {2} categories'.format(name, numPeriods, numCats)

def gen_desc_PastDiffNormRd(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])	
	return 'Change in {0} since {1} (Number of standard deviations above/below mean)'.format(name, periodDelta)

def gen_desc_PastLvl(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	numPeriods = kwargs.get(key, kwargDefaults[key])
	return 'Value of {0} {1} periods ago'.format(name, numPeriods)

def gen_desc_PastLvlCat(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	numPeriods = kwargs.get(key, kwargDefaults[key])
	key = NUM_RANGES
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'Value of {0} {1} periods ago (in {2} categories)'.format(name, numPeriods, numCats)

def gen_desc_PastLvlNormRd(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	numPeriods = kwargs.get(key, kwargDefaults[key])
	return 'Value of {0} {1} periods ago (Number of standard deviations above/below mean)'.format(name, numPeriods)

def gen_desc_FutrDiff(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	numPeriods = kwargs.get(key, kwargDefaults[key])
	return 'Change in {0} {1} periods ahead'.format(name, numPeriods)

def gen_desc_FutrDiffCat(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	key = NUM_RANGES
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'Change in {0} {1} periods ahead in {2} categories'.format(name, numPeriods, numCats)

def gen_desc_FutrDiffNormRd(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	periodDelta = kwargs.get(key, kwargDefaults[key])
	key = NUM_RANGES
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'Change in {0} {1} periods ahead (Number of standard deviations above/below mean)'.format(name, numPeriods)

def gen_desc_FutrLvl(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	numPeriods = kwargs.get(key, kwargDefaults[key])
	return 'Value of {0} {1} periods ahead'.format(name, numPeriods)

def gen_desc_FutrLvlCat(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	numPeriods = kwargs.get(key, kwargDefaults[key])
	key = NUM_RANGES
	numCats = kwargs.get(key, kwargDefaults[key])
	return 'Value of {0} {1} periods ago (in {2} categories)'.format(name, numPeriods, numCats)
	
def gen_desc_FutrLvlNormRd(kwargs, name):
	key = FIRST_ORDER_DIFF_TIME
	numPeriods = kwargs.get(key, kwargDefaults[key])
	return 'Value of {0} {1} periods ahead (Number of standard deviations above/below mean)'.format(name, numPeriods)


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
# 	print np.hstack((transform_TimeSinceValue(d, {TIME_SINCE_VALUE: 1}).reshape(len_,1),
# 					d.reshape(len_,1)))
