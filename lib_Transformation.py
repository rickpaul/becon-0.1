# TODO: 
#	Add transformations for time as well as data
#	How do we implement controls?
#		e.g. logarithms must be above zero

import util_Transformation as util_Trns


TRANS_P_GEOM_DIST = 0.75 # When creating random transformations, create n from geomdist where p = _ (mean=1/p)

# Template is (dataTransform, timeSeriesTransform, hashCode)
Transformations = {
	'None':					(util_Trns.transform_None, 						util_Trns.timeSeriesTransform_None, 		0),
	'Logarithm': 			(util_Trns.transform_Logarithm, 				util_Trns.timeSeriesTransform_None, 		1),
	'Absolute': 			(util_Trns.transform_AbsoluteValue, 			util_Trns.timeSeriesTransform_None, 		2),
	'FirstOrderDifference': (util_Trns.transform_FirstOrderDifference, 		util_Trns.timeSeriesTransform_Trailing, 	3),
	'NormDistLocation': 	(util_Trns.transform_NormalDistributionZScore, 	util_Trns.timeSeriesTransform_None, 		4),
}
TransformationKeys = Transformations.keys()

# Template is (dataCategorization, hashCode)
Categorizations = {
	'None': 				(util_Trns.categorize_None,					0),
	'Sign': 				(util_Trns.categorize_Sign,					1),
	'Round': 				(util_Trns.categorize_Round,				2),
	'Floor': 				(util_Trns.categorize_Floor,				3),
	# 'Ceil': 				(util_Trns.categorize_Ceiling,				4), # Don't want for now. Too broad.
	'uniformLengthRange':	(util_Trns.categorize_UniformLengthRange,	5),
	'uniformCountRange': 	(util_Trns.categorize_QuantileRange,		6),
}
CategorizationKeys = Categorizations.keys()

TransformationPatterns = {
	'None': (0, ('None',), 'None'),
	'RateOfChange': (1, ('FirstOrderDifference',), 'uniformLengthRange'),
	'RateOfAcceleration': (2, ('FirstOrderDifference', 'FirstOrderDifference'), 'uniformLengthRange'),
	'Stratification': (3, ('None',), 'uniformLengthRange'),
}

MAX_NUM_TRANSFORMATIONS = 100 	# power of 10 for easy hashing
MAX_NUM_CATEGORIZATIONS = 100	# power of 10 for easy hashing
MAX_TRANSFORMATIONS = 5