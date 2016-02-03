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
		self._trnsName = trnsPtrn
		self._trnsCode = trnsCode
		# For some reason _trnsKwargs was all pointing to same dict instance,
		# so different declarations of trns_Hndl were having inadvertent _trnsKwargs
		# changes. Copy fixed it.
		self._trnsKwargs = copy(trnsKwargs) 

	def __str__(self):
		return lib_Trns.TransformationNames[self._trnsName](self._trnsKwargs)

	def name():
		doc = "The name property."
		def fget(self):
			return self._trnsName
		return locals()
	name = property(**name())

	def code():
		doc = "The code property."
		def fget(self):
			return self._trnsCode
		return locals()
	code = property(**code())

	def parameters():
		doc = "The code property."
		def fget(self):
			return self._trnsKwargs
		return locals()
	parameters = property(**parameters())

	def set_extra_parameter(self, name, value):
		assert name in util_Trns.kwargDefaults
		self._trnsKwargs[name] = value

	def transform_data(self, dataSeries):
		'''
		'''
		for fn in self.dataTrnsList:
			dataSeries = fn(dataSeries, self._trnsKwargs)[util_Trns.DATA_KEY]
		categorizationData = self.categorization(dataSeries, self._trnsKwargs)
		self.dataSplits = categorizationData.get(util_Trns.SPLITS_KEY,None)
		return categorizationData[util_Trns.DATA_KEY]

	# Sloppy
	def reverse_transform_data(self, dataSeries, modifier=None):
		for fn in reversed(self.dataTrnsList):
			revFn = lib_Trns.TransformationReversals[fn]
			if modifier is not None:
				dataSeries = revFn(dataSeries, modifier, self._trnsKwargs)[util_Trns.DATA_KEY]
			else:
				dataSeries = revFn(dataSeries, self._trnsKwargs)[util_Trns.DATA_KEY]
		return dataSeries

	def prediction_is_value_dependent(self):
		and_ = lambda x,y: x and y
		return reduce(and_, [lib_Trns.TransformationReversals[fn] not in lib_Trns.IndependentTransformationReversals for fn in self.dataTrnsList])

	def transform_time(self, timeHandle):
		for fn in self.timeTrnsList:
			fn(timeHandle, self._trnsKwargs)

	def reverse_transform_time(self, timeHandle):
		for fn in reversed(self.timeTrnsList):
			revFn = lib_Trns.TimeTransformationReversals[fn]
			revFn(timeHandle, self._trnsKwargs)

	def is_bounded(self):
		return self.isBounded

	def __add_transformation(self, trns_name):
		(data_trns_fn, time_trns_fn) = lib_Trns.Transformations[trns_name]
		self.dataTrnsList.append(data_trns_fn)
		self.timeTrnsList.append(time_trns_fn)
		self._trnsName = trns_name

	def __set_categorization(self, cat_name):
		(cat_function, is_bounded) = lib_Trns.Categorizations[cat_name]
		self.categorization = cat_function
		self.isBounded = is_bounded
