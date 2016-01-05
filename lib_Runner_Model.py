# EMF 		Import...As
import 	lib_Transformation 		as lib_Trns


# When creating random transformations,
# create n from geomdist where p = _ (mean=1/p)
WORD_COUNT_GEOMETRIC_PARAM = 0.75
MIN_WORD_COUNT = 3

MIN_BATCH_SIZE = 4
MAX_BATCH_SIZE = 4

MODEL_RETENTION_THRESHHOLD = 0.3


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


TestModelTemplate = {
	'responseTicker' : ['y'],
	# 'responseTrns' : ['RateOfChange'],
	'responseKwargs': {
		'PeriodDiff': [1,3,6,9,12],
	},
	# 'predictorTrns' : ['Truncate', 'RateOfChange'],
	'predictorKwargs': {
		'PeriodDiff': [1,3,6,9,12],
	},
	'models' : ['RegrDecisionTree'],
	'dataSeriesCriteria' : {
		# 'interpolatePredictorData' : False,
		# 'matchResponsePeriodicity' : True,
		# 'periodicity' : 1,
		# 'categorical' : False
	}
}
