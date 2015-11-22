# TODO: 
#	IS HAVING TWO FIRST ORDER DIFFERENCES CORRECT?!
#	Add codes (for hashing)
#	Add transformations for time as well as data
#	How do we implement controls?
#		e.g. logarithms must be above zero

import EMF_Transformations_util as EMF_Trns


TRANS_P_GEOM_DIST = 0.75 # When creating random transformations, create n from geomdist where p = _ (mean=1/p)

# Template is (dataTransform, timeSeriesTransform, hashCode)
Transformations = {
	'None':					(EMF_Trns.transform_None, 						EMF_Trns.timeSeriesTransform_None, 		-1),
	'Logarithm': 			(EMF_Trns.transform_Logarithm, 					EMF_Trns.timeSeriesTransform_None, 		1),
	'Absolute': 			(EMF_Trns.transform_AbsoluteValue, 				EMF_Trns.timeSeriesTransform_None, 		2),
	'FirstOrderDifference': (EMF_Trns.transform_FirstOrderDifference, 		EMF_Trns.timeSeriesTransform_Trailing, 	3),
	'NormDistLocation': 	(EMF_Trns.transform_NormalDistributionZScore, 	EMF_Trns.timeSeriesTransform_None, 		4),
}
TransformationKeys = Transformations.keys()

# Template is (dataCategorization, hashCode)
Categorizations = {
	'None': 				(EMF_Trns.categorize_None,					-1),
	'Sign': 				(EMF_Trns.categorize_Sign,					1),
	'Round': 				(EMF_Trns.categorize_Round,					2),
	'Floor': 				(EMF_Trns.categorize_Floor,					3),
	# 'Ceil': 				(EMF_Trns.categorize_Ceiling,				4), # Don't want for now. Too broad.
	'uniformLengthRange':	(EMF_Trns.categorize_UniformLengthRange,	5),
	'uniformCountRange': 	(EMF_Trns.categorize_QuantileRange,			6),
}
CategorizationKeys = Categorizations.keys()

CommonTransformations = {
	'RateOfChange': (('FirstOrderDifference'), 'uniformLengthRange'),
	'RateOfAcceleration': (('FirstOrderDifference', 'FirstOrderDifference'), 'uniformLengthRange'),
	'Stratification': (('None',), 'uniformLengthRange'),
}
