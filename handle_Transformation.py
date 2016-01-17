# TODO:
# 	Create some model of transformation complexity? (i.e. O(n))

# EMF 		Import...As
import lib_Transformation 	as lib_Trns
import util_Transformation 	as util_Trns

# System 	From...Import
from copy 	import copy
from json 	import dumps 	as json_dump
from random import choice

class EMF_Transformation_Handle:
	def __init__(self, trnsPtrn, trnsKwargs={}):
		'''
		trnsSeries tuple<list<string>, string> is modeled off lib_Transformation.TransformationPatterns
		'''
		(trnsCode, trnsList, categorization) = lib_Trns.TransformationPatterns[trnsPtrn]
		self.dataTrnsList = []
		self.timeTrnsList = []	
		for t in trnsList:
			self.__add_transformation(t)
		self.__set_categorization(categorization)
		self.trnsName = trnsPtrn
		self.trnsCode = trnsCode
		# For some reason trnsKwargs was all pointing to same dict instance,
		# so different declarations of trns_Hndl were having inadvertent trnsKwargs
		# changes. Copy fixed it.
		self.trnsKwargs = copy(trnsKwargs) 

	def __str__(self):
		return lib_Trns.TransformationNames[self.trnsName](self.trnsKwargs)

	def set_extra_parameter(self, name, value):
		assert name in util_Trns.kwargDefaults
		self.trnsKwargs[name] = value

	def transform_data(self, dataSeries):
		'''
		'''
		for fn in self.dataTrnsList:
			dataSeries = fn(dataSeries, self.trnsKwargs)
		dataSeries = self.categorization(dataSeries, self.trnsKwargs)
		return dataSeries
	
	def reverse_transform_data(self, dataSeries, predictionDelta=None):
		for fn in reversed(self.dataTrnsList):
			revFn = lib_Trns.TransformationReversals[fn]
			if predictionDelta is not None:
				dataSeries = revFn(dataSeries, predictionDelta, self.trnsKwargs)
			else:
				dataSeries = revFn(dataSeries, self.trnsKwargs)
		return dataSeries

	def prediction_is_value_dependent(self):
		and_ = lambda x,y: x and y
		return reduce(and_, [lib_Trns.TransformationReversals[fn] in IndependentTransformationReversals for fn in self.dataTrnsList])

	def transform_time(self, timeHandle):
		'''
		TODO:
					Make/return a copy of timeHandle?
		'''
		for fn in self.timeTrnsList:
			fn(timeHandle, self.trnsKwargs)

	def reverse_transform_time(self, timeHandle):
		'''
		TODO:
					Make/return a copy of timeHandle?
		'''
		for fn in reversed(self.timeTrnsList):
			revFn = lib_Trns.TimeTransformationReversals[fn]
			revFn(timeHandle, self.trnsKwargs)

	def is_bounded(self):
		return self.isBounded

	def __add_transformation(self, trns_name):
		(data_trns_fn, time_trns_fn) = lib_Trns.Transformations[trns_name]
		self.dataTrnsList.append(data_trns_fn)
		self.timeTrnsList.append(time_trns_fn)
		self.trnsName = trns_name

	def __set_categorization(self, cat_name):
		(cat_function, is_bounded) = lib_Trns.Categorizations[cat_name]
		self.categorization = cat_function
		self.isBounded = is_bounded

	def __transform(self, function, series):
		'''
		'''
		return function(series, self.trnsKwargs)

