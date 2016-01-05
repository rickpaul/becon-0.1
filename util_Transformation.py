'''
TODOS:
	+ How do you find quantiles numpy?
'''
# EMF 		From...Import
from 	util_EMF 	import YEARS, QUARTERS, MONTHS, WEEKS, DAYS
from 	util_EMF 	import dt_add_months, dt_subtract_months
from 	util_EMF 	import dt_epoch_to_datetime, dt_datetime_to_epoch
# EMF 		Import...As
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

def transform_FOD_BackwardLooking(data, kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return data[periodDelta:] - data[:-periodDelta]

def transform_FOD_ForwardLooking(data, kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return data[:-periodDelta] - data[periodDelta:]

def transform_Level_Backwards(data, kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return data[:-periodDelta]	

def transform_Level_Forwards(data, kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return data[periodDelta:]

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

def timeSeriesTransform_TruncatePast(timeSeries, kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return timeSeries[periodDelta:]

def timeSeriesTransform_TruncateFuture(timeSeries, kwargs):
	key = 'PeriodDiff'
	periodDelta = kwargs.get(key, kwargDefaults[key])
	return timeSeries[:-periodDelta]

def timeSeriesTransform_None(timeSeries, kwargs):
	return timeSeries

def timePointTransform_EarliestDate(date, periodicity, fn, kwargs):
	if fn == timeSeriesTransform_TruncatePast:
		key = 'PeriodDiff'
		periodDelta = kwargs.get(key, kwargDefaults[key])
		dt_ = dt_epoch_to_datetime(date)
		if periodicity == MONTHS:
			dt_ = dt_subtract_months(dt_, periodDelta)
			return dt_datetime_to_epoch(dt_)
		elif periodicity == YEARS:
			dt_ = dt_subtract_months(dt_, periodDelta*12)
			return dt_datetime_to_epoch(dt_)
		elif periodicity == QUARTERS:
			dt_ = dt_subtract_months(dt_, periodDelta*3)
			return dt_datetime_to_epoch(dt_)
		elif periodicity == DAYS or periodicity == WEEKS:
			raise NotImplementedError
		else:
			log.warning('Periodicity not recognized.')
			return date+periodicity*periodDelta
	else:
		return date

def timePointTransform_LatestDate(date, periodicity, fn, kwargs):
	if fn == timeSeriesTransform_TruncateFuture:
		key = 'PeriodDiff'
		periodDelta = kwargs.get(key, kwargDefaults[key])
		dt_ = dt_epoch_to_datetime(date)
		if periodicity == MONTHS:
			dt_ = dt_subtract_months(dt_, periodDelta)
			return dt_datetime_to_epoch(dt_)
		elif periodicity == YEARS:
			dt_ = dt_subtract_months(dt_, periodDelta*12)
			return dt_datetime_to_epoch(dt_)
		elif periodicity == QUARTERS:
			dt_ = dt_subtract_months(dt_, periodDelta*3)
			return dt_datetime_to_epoch(dt_)
		elif periodicity == DAYS or periodicity == WEEKS:
			raise NotImplementedError
		else:
			log.warning('Periodicity not recognized.')
			return date-periodicity*periodDelta
	else:
		return date


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

