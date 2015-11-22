# TODO:
#	PRIORITY: GET ACTUAL TRANSFORMATION HASH, not RANDOM!!!!
#	IMPORTANT! Does secondary Transformation for FirstOrderDiff get parameter?
# 	Create some model of transformation complexity?
# 	Why do we care if transformationHandle isSet?
#	CONSIDER: Should we just have a list of transformations, rather than three layers?

import EMF_Transformations_lib as EMF_Trns
from json 	import dumps 	as json_dump
from random import choice

class EMF_Transformation_Handle:
	def __init__(self):
		self.__reset()

	def __reset(self):
		self.dataTransformations = []
		self.timeTransformations = []
		self.categorization = None
		self.hashComponents = [[], None, []]
		self.stringComponents = [[], None, []]
		self.extraParameters = {}

	def unsetTransformation(self):
		self.__reset()

	def isSet(self):
		return (len(self.dataTransformations) > 0) and (self.categorization is not None)

	def addTransformation_named(self, trans_name):
		(dataTransform, timeSeriesTransform, hashCode) = EMF_Trns.Transformations[trans_name]
		self.dataTransformations.append(dataTransform)
		self.timeTransformations.append(timeSeriesTransform)
		self.hashComponents[0].append(hashCode)
		self.stringComponents[0].append(trans_name)

	def addTransformation_random(self):
		trans_name = choice(EMF_Trns.TransformationKeys)
		self.addTransformation_named(trans_name)

	def setCategorization(self, cat_name):
		(dataCategorization, hashCode) = EMF_Trns.Categorizations[cat_name]
		self.hashComponents[1] = hashCode
		self.stringComponents[1] = cat_name
		self.categorization = dataCategorization

	def randomizeCategorization(self):
		cat_name = choice(EMF_Trns.CategorizationKeys)
		self.setCategorization(cat_name)

	def setExtraParameter(self, parameterName, parameterValue):
		assert parameterName in EMF_Trns.availableKeywordArgs
		self.extraParameters[parameterName] = parameterValue

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
		# (transformations, categorization, extraParameters)
		return choice(xrange(200)) #TODO: FIX! THIS IS REALLY BAD! HACK!