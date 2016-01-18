# EMF 		From...Import
from 	lib_TimeSet		 	import DAYS, WEEKS, MONTHS, QUARTERS, YEARS
# EMF 		Import...As
import 	lib_Transformation 	as lib_Trns

# When creating random transformations,
# create n from geomdist where p = _ (mean=1/p)
WORD_COUNT_GEOMETRIC_PARAM = 0.75
MIN_WORD_COUNT = 3

MIN_BATCH_SIZE = 4
MAX_BATCH_SIZE = 4

MODEL_RETENTION_THRESHHOLD = 0.3
BOOTSTRAP_MULTIPLIER = 1

TRAINING = 927610 # Random
PREDICTION = 176092 # Random
PREDICTION_DEPENDENT = 290761 # Random. # Will probably be deleted. Nec. for current spaghetti

PredictorTransformationKeys = lib_Trns.PredictorTransformationKeys
PredictorTransformationKeys = [x for x in PredictorTransformationKeys if not x.endswith(lib_Trns.PATTERN_SUFFIX_NORM_STRAT)]
PredictorTransformationKeys = [x for x in PredictorTransformationKeys if not x.endswith(lib_Trns.PATTERN_SUFFIX_STRAT)]

ResponseTransformationKeys = lib_Trns.ResponseTransformationKeys
ResponseTransformationKeys = [x for x in ResponseTransformationKeys if  x.startswith(lib_Trns.PATTERN_PREFIX_FUTURE)]
ResponseTransformationKeys = [x for x in ResponseTransformationKeys if not x.endswith(lib_Trns.PATTERN_SUFFIX_NORM_STRAT)]
ResponseTransformationKeys = [x for x in ResponseTransformationKeys if not x.endswith(lib_Trns.PATTERN_SUFFIX_STRAT)]
try:
	idx = ResponseTransformationKeys.index('Futr_Acc')
	del ResponseTransformationKeys[idx]
except ValueError:
	pass # Value not found

TimeToRecTemplate = {
	'responseTicker' : ['US_TimeUntilRec'],
	'responseTrns' : ['None', 'Futr_Lvl'],
	'responseKwargs': {
		'PeriodDiff': [1,3,6,9,12],
		'numRanges': [5]
	},
	# 'predictorTrns' : [ 'RateOfChange'],
	'predictorKwargs': {
		'PeriodDiff': [1,3,6,9,12],
	},
	'models' : ['RegrDecisionTree'],
	'predictorCriteria' : {
		# 'interpolatePredictorData' : False,
		# 'matchResponsePeriodicity' : True,
		'periodicity' : MONTHS,
		# 'categorical' : False
	}
}

SP500Template = {
	'responseTicker' : ['SP500_RealPrice'],
	'responseTrns' : ['None', 'Futr_Lvl'],
	'responseKwargs': {
		'PeriodDiff': [1,3,6,9,12],
		'numRanges': [5]
	},
	'responseCanPredict' : True,
	# 'predictorTrns' : [ 'RateOfChange'],
	'predictorKwargs': {
		'PeriodDiff': [1,3,6,9,12],
	},
	'models' : ['RegrDecisionTree'],
	'predictorCriteria' : {
		# 'matchResponsePeriodicity' : True,
		'periodicity' : MONTHS,
		# 'categorical' : False
		'minDate' : None,
		'maxDate' : None,
	}
}



