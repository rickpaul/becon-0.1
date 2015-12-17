# TODO:
#	IMPORTANT! Does secondary Transformation for FirstOrderDiff get parameter?
# 	Create some model of transformation complexity? (i.e. O(n))


import lib_Transformation as lib_Trns
from json 	import dumps 	as json_dump
from random import choice

class EMF_Transformation_Handle:
	def __init__(self):
		self.unset_Transformation()

	def __str__(self):
		return self.transformationName

	def unset_Transformation(self):
		self.transformationName = None
		self.dataTransformations = []
		self.timeTransformations = []
		self.categorization = None
		self.hashComponents = [[], None, []]
		self.stringComponents = [[], None, []]
		self.extraParameters = {}

	def is_set(self):
		return (len(self.dataTransformations) > 0) and (self.categorization is not None)

	def addTransformation_named(self, trans_name):
		(dataTransform, timeSeriesTransform, hashCode) = lib_Trns.Transformations[trans_name]
		self.dataTransformations.append(dataTransform)
		self.timeTransformations.append(timeSeriesTransform)
		self.hashComponents[0].append(hashCode)
		self.stringComponents[0].append(trans_name)
		self.transformationName = trans_name

	def addTransformation_random(self):
		trans_name = choice(lib_Trns.TransformationKeys)
		self.addTransformation_named(trans_name)

	def setCategorization(self, cat_name):
		(dataCategorization, hashCode) = lib_Trns.Categorizations[cat_name]
		self.hashComponents[1] = hashCode
		self.stringComponents[1] = cat_name
		self.categorization = dataCategorization

	def randomizeCategorization(self):
		cat_name = choice(lib_Trns.CategorizationKeys)
		self.setCategorization(cat_name)

	def setExtraParameter(self, parameterName, parameterValue):
		assert parameterName in lib_Trns.availableKeywordArgs
		self.extraParameters[parameterName] = parameterValue
		raise NotImplementedError # We don't know how to hash this yet

	def transformDataSeries(self, dataSeries):
		'''
		'''
		for transformation in self.dataTransformations:
			dataSeries = self.__doSingleTransformation(transformation, dataSeries)
		dataSeries = self.__doSingleTransformation(self.categorization, dataSeries)
		return dataSeries

	def transformTimeSeries(self, timeSeries):
		for transformation in self.timeTransformations:
			timeSeries = self.__doSingleTransformation(transformation, timeSeries)
		return timeSeries

	def __doSingleTransformation(self, transformation, series):
		'''
		'''
		return transformation(series, self.extraParameters)

	def getTransformation_asString(self):
		'''
		Returns a string-filled list of transformations this handle has, in the tuple<list<string>, string> form
		'''
		assert self.isSet()
		raise NotImplementedError

	def getTransformation_asJSON(self):
		'''
		Returns a string-filled list of transformations this handle has, in the tuple<list<string>, string> form
		'''
		assert self.isSet()
		return json_dump(self.stringComponents)

	def getTransformation_asHash(self):
		'''
		Returns a string hash of transformations this handle has
		# TODO: change to integer hash
		'''
		assert self.isSet()
		(transformations, categorization, extraParameters) = self.hashComponents
		posCounter = 0
		hashNum = 0
		# Add Transformations
		for i in xrange(len(transformations)):
			hashNum += lib_Trns.MAX_NUM_TRANSFORMATIONS^posCounter*transformations
		posCounter = lib_Trns.MAX_TRANSFORMATIONS
		# Add Categorization
		hashNum +=  lib_Trns.MAX_NUM_CATEGORIZATIONS^posCounter
		# Add Parameters
		raise NotImplementedError


