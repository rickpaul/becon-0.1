# TODO:
#	IMPORTANT! Does secondary Transformation for FirstOrderDiff get parameter?
# 	Create some model of transformation complexity? (i.e. O(n))

# EMF 		Import...As
import lib_Transformation 	as lib_Trns
import util_Transformation 	as util_Trns

# System 	From...Import
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
		self.trnsKwargs = trnsKwargs

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

	def transform_time(self, timeSeries):
		for fn in self.timeTrnsList:
			timeSeries = self.__transform(fn, timeSeries)
		return timeSeries

	def transform_earliest_time(self, dte, periodicity):
		for fn in self.timeTrnsList:
			dte = util_Trns.timePointTransform_EarliestDate(dte, periodicity, fn, self.trnsKwargs)
		return dte

	def transform_latest_time(self, dte, periodicity):
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

