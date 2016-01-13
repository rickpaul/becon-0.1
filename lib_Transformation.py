# TODO: 
#	Implement Controls
#		e.g. logarithms must be above zero

# EMF 		Import...As
import util_Transformation as util_Trns

# Template is (dataTransform, timeSeriesTransform)
Transformations = {
	'None':					(util_Trns.transform_None, 						util_Trns.timeSeriesTransform_None,),
	'Logarithm': 			(util_Trns.transform_Logarithm, 				util_Trns.timeSeriesTransform_None,),
	'Absolute': 			(util_Trns.transform_AbsoluteValue, 			util_Trns.timeSeriesTransform_None,),
	'Level_Past': 			(util_Trns.transform_Level_Backwards, 			util_Trns.timeSeriesTransform_TruncatePast,),
	'Level_Future': 		(util_Trns.transform_Level_Forwards, 			util_Trns.timeSeriesTransform_TruncateFuture,),
	'FOD_Past': 			(util_Trns.transform_FOD_BackwardLooking, 		util_Trns.timeSeriesTransform_TruncatePast,),
	'FOD_Future': 			(util_Trns.transform_FOD_ForwardLooking, 		util_Trns.timeSeriesTransform_TruncateFuture,),
	'NormDistLocation': 	(util_Trns.transform_NormalDistributionZScore, 	util_Trns.timeSeriesTransform_None,),
}
TransformationKeys = Transformations.keys()

# Template is (dataCategorization, isBounded)
Categorizations = {
	'None': 				(util_Trns.categorize_None,					False),
	'Sign': 				(util_Trns.categorize_Sign,					False),
	'Int_Round': 			(util_Trns.categorize_Round,				False),
	'Int_Floor': 			(util_Trns.categorize_Floor,				False),
	# 'Int_Ceil': 			(util_Trns.categorize_Ceiling,				False), # Don't want for now. Too broad.
	'uniformLengthRange':	(util_Trns.categorize_UniformLengthRange,	True),
	'uniformCountRange': 	(util_Trns.categorize_QuantileRange,		True),
}
CategorizationKeys = Categorizations.keys()

TransformationPatterns = {
	'None': 					(0, ('None',), 'None'),
	
	'Past_Change': 				(1, ('FOD_Past',), 'None'),
	'Past_Change_Cat': 			(2, ('FOD_Past',), 'uniformLengthRange'),
	'Past_Change_NormRd': 		(3, ('FOD_Past','NormDistLocation'), 'Int_Round'),

	# 'Past_Acc': 				(4, ('Logarithm', 'FOD_Past'), 'None'),
	# 'Past_Acc_Cat': 			(5, ('Logarithm', 'FOD_Past'), 'uniformLengthRange'),
	# 'Past_Acc_NormRd':			(6, ('Logarithm', 'FOD_Past','NormDistLocation'), 'Int_Round'),

	'Current_Lvl_Cat': 			(7, ('None',), 'uniformLengthRange'),
	'Current_Lvl_NormRd': 		(8, ('NormDistLocation',), 'Int_Round'),

	'Past_Lvl': 				(9, ('Level_Past',), 'None'),
	'Past_Lvl_Cat': 			(11, ('Level_Past',), 'uniformLengthRange'),
	'Past_Lvl_NormRd': 			(12, ('Level_Past', 'NormDistLocation',), 'Int_Round'),

	'Futr_Lvl': 				(13, ('Level_Future',), 'None'),
	'Futr_Lvl_Cat': 			(14, ('Level_Future',), 'uniformLengthRange'),
	'Futr_Lvl_NormRd': 			(15, ('Level_Future', 'NormDistLocation',), 'Int_Round'),
	
	'Futr_Change': 				(16, ('FOD_Future',), 'None'),
	'Futr_Change_Cat': 			(17, ('FOD_Future',), 'uniformLengthRange'),
	'Futr_Change_NormRd': 		(18, ('FOD_Future','NormDistLocation'), 'Int_Round'),

	# 'Futr_Acc': 				(19, ('Logarithm', 'FOD_Future'), 'None'),
	# 'Futr_Acc_Cat': 			(20, ('Logarithm', 'FOD_Future'), 'uniformLengthRange'),
	# 'Futr_Acc_NormRd':			(21, ('Logarithm', 'FOD_Future','NormDistLocation'), 'Int_Round'),
}
TransformationPatternsKeys = TransformationPatterns.keys()

PATTERN_PREFIX_FUTURE = 'Futr_'
PATTERN_SUFFIX_STRAT = '_Cat'
PATTERN_SUFFIX_NORM_STRAT = '_NormRd'

ResponseTransformationKeys = TransformationPatternsKeys
PredictorTransformationKeys = [x for x in TransformationPatternsKeys if not x.startswith(PATTERN_PREFIX_FUTURE)]

TransformationNames = {
	'None': 					util_Trns.transformStr_None,
	
	'Past_Change': 				util_Trns.transformStr_PastDiff,
	'Past_Change_Cat': 			util_Trns.transformStr_PastDiffCat,
	'Past_Change_NormRd': 		util_Trns.transformStr_PastDiffNormRd,

	# 'Past_Acc': 				(4, ('Logarithm', 'FOD_Past'), 'None'),
	# 'Past_Acc_Cat': 			(5, ('Logarithm', 'FOD_Past'), 'uniformLengthRange'),
	# 'Past_Acc_NormRd':			(6, ('Logarithm', 'FOD_Past','NormDistLocation'), 'Int_Round'),

	'Current_Lvl_Cat': 			util_Trns.transformStr_Cat,
	'Current_Lvl_NormRd': 		util_Trns.transformStr_NormRd,

	'Past_Lvl': 				util_Trns.transformStr_PastLvl,
	'Past_Lvl_Cat': 			util_Trns.transformStr_PastLvlCat,
	'Past_Lvl_NormRd': 			util_Trns.transformStr_PastLvlNormRd,

	'Futr_Lvl': 				util_Trns.transformStr_FutrLvl,
	'Futr_Lvl_Cat': 			util_Trns.transformStr_FutrLvlCat,
	'Futr_Lvl_NormRd': 			util_Trns.transformStr_FutrLvlNormRd,
	
	'Futr_Change': 				util_Trns.transformStr_FutrDiff,
	'Futr_Change_Cat': 			util_Trns.transformStr_FutrDiffCat,
	'Futr_Change_NormRd': 		util_Trns.transformStr_FutrDiffNormRd,

	# 'Futr_Acc': 				(19, ('Logarithm', 'FOD_Future'), 'None'),
	# 'Futr_Acc_Cat': 			(20, ('Logarithm', 'FOD_Future'), 'uniformLengthRange'),
	# 'Futr_Acc_NormRd':			(21, ('Logarithm', 'FOD_Future','NormDistLocation'), 'Int_Round'),
}

TransformationReversals = {
	util_Trns.transform_None: util_Trns.transform_usePredictions,
	util_Trns.transform_Level_Backwards: util_Trns.transform_usePredictions,
	util_Trns.transform_Level_Forwards: util_Trns.transform_usePredictions,
	util_Trns.transform_FOD_BackwardLooking: util_Trns.transform_SubtractSeries,
	util_Trns.transform_FOD_ForwardLooking: util_Trns.transform_AddSeries,
}

TimeTransformationReversals = {
	util_Trns.timeSeriesTransform_None: util_Trns.transform_None,
	util_Trns.timeSeriesTransform_TruncatePast: util_Trns.timeSeriesTransform_ShiftPast,
	util_Trns.timeSeriesTransform_TruncateFuture: util_Trns.timeSeriesTransform_ShiftFuture,

}


# HASHING CONSTANTS
# MAX_NUM_TRANSFORMATIONS = 100 	# power of 10 for easy hashing
# MAX_NUM_CATEGORIZATIONS = 100	# power of 10 for easy hashing
# TRANSFORMATION RANDOMIZATION CONSTANTS
# MAX_TRANSFORMATIONS = 5