# EMF 		From...Import
from 	lib_TimeSet		 	import DAYS, WEEKS, MONTHS, QUARTERS, YEARS
# EMF 		Import...As
import 	lib_Transformation 	as lib_Trns
import 	util_Transformation as utl_Trns
# System 	From...Import
from 	copy 				import deepcopy

# When creating random transformations,
# create n from geomdist where p = _ (mean=1/p)
PRED_COUNT_GEOMETRIC_PARAM	= 0.75
PRED_COUNT_FLOOR 			= 3
RESP_COUNT_GEOMETRIC_PARAM	= 0.75
RESP_COUNT_FLOOR 			= 0

MIN_BATCH_SIZE 				= 10
MAX_BATCH_SIZE 				= 20

MODEL_RETENTION_THRESHHOLD 	= 0.3
BOOTSTRAP_MULTIPLIER 		= 1

TRAINING 					= 'T'
PREDICTION_INDEPENDENT 		= 'PI'
PREDICTION_DEPENDENT 		= 'PD'

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

TemplateDefaults = {
	'responseCanPredict' : True,
	'responseTrns' : ['None', 'Futr_Lvl', 'Futr_Change'],
	'responseKwargs': {
		utl_Trns.FIRST_ORDER_DIFF_TIME: [1,3,6,9,12,18,24],
		utl_Trns.PERIODS_AWAY: [1,3,6,9,12,18,24],
		utl_Trns.NUM_RANGES: [5]
	},	
	# 'predictorTrns' : [ 'RateOfChange'],
	'predictorCriteria' : {
		# 'matchResponsePeriodicity' : True,
		'periodicity' : MONTHS,
		# 'categorical' : False
		'minDate' : None,
		'maxDate' : None,
	}
}


TimeToRecTemplate = deepcopy(TemplateDefaults)
TimeToRecTemplate.update({
	'responseTicker' : ['US_TimeUntilRec'],
	# 'responseTrns' : ['None', 'Futr_Lvl'],
	'models' : ['LinearRegression'],
})

SP500Template = deepcopy(TemplateDefaults)
SP500Template.update({
	'responseTicker' : ['SP500_RealPrice'],
	'models' : ['RegrDecisionTree'],
})



