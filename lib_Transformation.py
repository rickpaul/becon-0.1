# TODO: 
#	Implement Controls
#		e.g. logarithms must be above zero
# 	Level back and level forward transformations are truncating, for lack of good date functions

# EMF 		Import...As
import util_Transformation as util_Trns

# Template is (dataTransform, timeSeriesTransform)
Transformations = {
	'None':					(util_Trns.transform_None, 						util_Trns.timeSeriesTransform_None,),
	'Logarithm': 			(util_Trns.transform_Logarithm, 				util_Trns.timeSeriesTransform_None,),
	'Absolute': 			(util_Trns.transform_AbsoluteValue, 			util_Trns.timeSeriesTransform_None,),
	'Level_Past': 			(util_Trns.transform_None, 						util_Trns.timeSeriesTransform_ShiftFuture_Level,),
	'Level_Future': 		(util_Trns.transform_None, 						util_Trns.timeSeriesTransform_ShiftPast_Level,),
	'FOD_Past': 			(util_Trns.transform_FOD_BackwardLooking, 		util_Trns.timeSeriesTransform_TruncatePast,),
	'FOD_Future': 			(util_Trns.transform_FOD_ForwardLooking, 		util_Trns.timeSeriesTransform_TruncateFuture,),
	# 'Trailing_Vol': 		(util_Trns., 		util_Trns.timeSeriesTransform_TruncatePast,),
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
	'Futr_Lvl_NormR d': 			(15, ('Level_Future', 'NormDistLocation',), 'Int_Round'),
	
	'Futr_Change': 				(16, ('FOD_Future',), 'None'),
	'Futr_Change_Cat': 			(17, ('FOD_Future',), 'uniformLengthRange'),
	'Futr_Change_NormRd': 		(18, ('FOD_Future','NormDistLocation'), 'Int_Round'),

	# 'Futr_Acc': 				(19, ('Logarithm', 'FOD_Future'), 'None'),
	# 'Futr_Acc_Cat': 			(20, ('Logarithm', 'FOD_Future'), 'uniformLengthRange'),
	# 'Futr_Acc_NormRd':			(21, ('Logarithm', 'FOD_Future','NormDistLocation'), 'Int_Round'),

	# 'High_Vol': 				(22, )
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

	# 'Past_Acc': 				None,
	# 'Past_Acc_Cat': 			None,
	# 'Past_Acc_NormRd':		None,

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

	# 'Futr_Acc': 				None,
	# 'Futr_Acc_Cat': 			None,
	# 'Futr_Acc_NormRd':		None,
}

TransformationReversals = {
	util_Trns.transform_None: 						util_Trns.transform_usePredictions,
	util_Trns.transform_FOD_BackwardLooking: 		util_Trns.transform_SubtractSeries,
	util_Trns.transform_FOD_ForwardLooking: 		util_Trns.transform_AddSeries,
}

IndependentTransformationReversals = [
	util_Trns.transform_usePredictions,
]

TimeTransformationReversals = {
	util_Trns.timeSeriesTransform_None: 				util_Trns.transform_None,
	util_Trns.timeSeriesTransform_ShiftPast_Level: 		util_Trns.timeSeriesTransform_ShiftFuture_Level,
	util_Trns.timeSeriesTransform_ShiftFuture_Level: 	util_Trns.timeSeriesTransform_ShiftPast_Level,
	util_Trns.timeSeriesTransform_TruncatePast: 		util_Trns.timeSeriesTransform_ShiftPast_Change,
	util_Trns.timeSeriesTransform_TruncateFuture: 		util_Trns.timeSeriesTransform_ShiftFuture_Change,
}

TransformationDescs = {
	'None': 					(util_Trns.gen_desc_None, util_Trns.spec_desc_None),
	
	'Past_Change': 				(util_Trns.gen_desc_PastDiff, util_Trns.spec_desc_PastDiff),
	'Past_Change_Cat': 			(util_Trns.gen_desc_PastDiffCat, util_Trns.spec_desc_PastDiffCat),
	'Past_Change_NormRd': 		(util_Trns.gen_desc_PastDiffNormRd, util_Trns.spec_desc_PastDiffNormRd),

	'Current_Lvl_Cat': 			(util_Trns.gen_desc_Cat, util_Trns.spec_desc_Cat),
	'Current_Lvl_NormRd': 		(util_Trns.gen_desc_NormRd, util_Trns.spec_desc_NormRd),

	'Past_Lvl': 				(util_Trns.gen_desc_PastLvl, util_Trns.spec_desc_PastLvl),
	'Past_Lvl_Cat': 			(util_Trns.gen_desc_PastLvlCat, util_Trns.spec_desc_PastLvlCat),
	'Past_Lvl_NormRd': 			(util_Trns.gen_desc_PastLvlNormRd, util_Trns.spec_desc_PastLvlNormRd),

	'Futr_Lvl': 				(util_Trns.gen_desc_FutrLvl, util_Trns.spec_desc_FutrLvl),
	'Futr_Lvl_Cat': 			(util_Trns.gen_desc_FutrLvlCat, util_Trns.spec_desc_FutrLvlCat),
	'Futr_Lvl_NormRd': 			(util_Trns.gen_desc_FutrLvlNormRd, util_Trns.spec_desc_FutrLvlNormRd),
	
	'Futr_Change': 				(util_Trns.gen_desc_FutrDiff, util_Trns.spec_desc_FutrDiff),
	'Futr_Change_Cat': 			(util_Trns.gen_desc_FutrDiffCat, util_Trns.spec_desc_FutrDiffCat),
	'Futr_Change_NormRd': 		(util_Trns.gen_desc_FutrDiffNormRd, util_Trns.spec_desc_FutrDiffNormRd),
}


