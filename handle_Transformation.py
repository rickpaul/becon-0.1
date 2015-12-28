# TODO:
#	IMPORTANT! Does secondary Transformation for FirstOrderDiff get parameter?
# 	Create some model of transformation complexity? (i.e. O(n))

# EMF 		Import...As
import lib_Transformation as lib_Trns
# System 	From...Import
from json 	import dumps 	as json_dump
from random import choice

class EMF_Transformation_Handle:
	def __init__(self, transformationPatternName):
		'''
		trnsSeries tuple<list<string>, string> is modeled off lib_Transformation.TransformationPatterns
		'''
		(transformationPatternCode, transList, categorization) = lib_Trns.TransformationPatterns[transformationPatternName]
		self.dataTransformations = []
		self.timeTransformations = []	
		for transformation in transList:
			self.__add_transformation(transformation)
		self.__set_categorization(categorization)
		self.transformationName = transformationPatternName
		self.transformationCode = transformationPatternCode
		self.extraParameters = {}

	def __str__(self):
		return self.transformationName

	def set_extra_parameter(self, name, value):
		assert name in lib_Trns.availableKeywordArgs
		self.extraParameters[name] = value

	def transform_data(self, dataSeries):
		'''
		'''
		for function in self.dataTransformations:
			dataSeries = self.__transform(function, dataSeries)
		dataSeries = self.__transform(self.categorization, dataSeries)
		return dataSeries

	def transform_time(self, timeSeries):
		for function in self.timeTransformations:
			timeSeries = self.__transform(function, timeSeries)
		return timeSeries

	def __add_transformation(self, trns_name):
		(data_trns_fn, time_trns_fn, trns_code) = lib_Trns.Transformations[trns_name]
		self.dataTransformations.append(data_trns_fn)
		self.timeTransformations.append(time_trns_fn)
		self.transformationName = trns_name

	def __set_categorization(self, cat_name):
		(cat_function, cat_code) = lib_Trns.Categorizations[cat_name]
		self.categorization = cat_function

	def __transform(self, function, series):
		'''
		'''
		return function(series, self.extraParameters)

