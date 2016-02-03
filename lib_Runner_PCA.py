# EMF 		From...Import
from 	lib_TimeSet		 	import DAYS, WEEKS, MONTHS, QUARTERS, YEARS
# EMF 		Import...As
import 	util_Transformation as utl_Trns
# System 	From...Import
from 	copy 				import deepcopy

# PD Column Name
IS_INTERPOLATED = 'is_int_'

# Interpolations
LINEAR 		= 'linear'
LAST_VALUE 	= 'zero'
NEAREST 	= 'nearest'

TemplateDefaults = {
	'responseCanPredict' : True,
	'responseTrns' : ['None', 'Futr_Lvl', 'Futr_Change'],
	'responseKwargs': {
		utl_Trns.FIRST_ORDER_DIFF_TIME: [1,3,6,9,12,18,24],
		utl_Trns.PERIODS_AWAY: [1,3,6,9,12,18,24],
		utl_Trns.NUM_RANGES: [5]
	},	
	# 'predictorTrns' : [ 'Past_Lvl', 'Past_Change'],
	'predictorCriteria' : {
		# 'matchResponsePeriodicity' : True,
		'periodicity' : MONTHS,
		# 'categorical' : False
		'minDate' : None,
		'maxDate' : None,
	},
	'responseCriteria' : {
		# 'matchResponsePeriodicity' : True,
		# 'periodicity' : MONTHS,
		# 'categorical' : False
		# 'minDate' : None,
		# 'maxDate' : None,
	}
}


BusCycleTemplate = deepcopy(TemplateDefaults)
BusCycleTemplate.update({
	'responseTickers' : ['US_TimeUntilRec','US_TimeUntilRec'],
	# 'responseTrns' : ['None', 'Futr_Lvl'],
})