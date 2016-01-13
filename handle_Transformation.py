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
			dataSeries = self.__transform(fn, dataSeries)
		dataSeries = self.__transform(self.categorization, dataSeries)
		return dataSeries
	
	def reverse_transform_data(self, dataSeries, predictionDelta=None):
		for fn in reversed(self.dataTrnsList):
			revFn = lib_Trns.TransformationReversals[fn]
			if predictionDelta is not None:
				dataSeries = revFn(dataSeries, predictionDelta, self.trnsKwargs)
			else:
				dataSeries = revFn(dataSeries, self.trnsKwargs)
		return dataSeries

	def transform_time(self, timeSeries):
		for fn in self.timeTrnsList:
			timeSeries = self.__transform(fn, timeSeries)
		return timeSeries

	def reverse_transform_time(self, timeSeries):
		for fn in reversed(self.timeTrnsList):
			revFn = lib_Trns.TimeTransformationReversals[fn]
			timeSeries = self.__transform(revFn, timeSeries)
		return timeSeries

	def transform_earliest_time(self, dte, periodicity):
		'''
		TODO:
					rename to make clear this is for domain, not range.
					add range function
		'''
		for fn in self.timeTrnsList:
			dte = util_Trns.timePointTransform_EarliestDate(dte, periodicity, fn, self.trnsKwargs)
		return dte

	def transform_latest_time(self, dte, periodicity):
		'''
		TODO:
					rename to make clear this is for domain, not range.
					add range function
		'''
		for fn in self.timeTrnsList:
			dte = util_Trns.timePointTransform_LatestDate(dte, periodicity, fn, self.trnsKwargs)
		return dte

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

