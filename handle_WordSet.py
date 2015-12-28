# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Transformation	import EMF_Transformation_Handle
from 	handle_WordSeries		import EMF_WordSeries_Handle
from 	lib_DBInstructions		import TICKER, retrieve_DataSeries_Filtered
from 	lib_Runner_Model		import WORD_COUNT_GEOMETRIC_PARAM
from 	lib_Transformation 		import TransformationPatterns
from 	util_WordSeries			import generate_Word_Series_name
# EMF 		Import...As
# System 	Import...As
# System 	From...Import
from 	numpy.random 			import geometric
from 	random 					import choice

class EMF_WordSet_Handle():
	def __init__(self, dbHandle):
		self.hndl_DB = dbHandle
		self.depWordCache = {}
		# self.periodicity = None
		self.indTrnsHandle = None
		self.indDataHandle = None
		self.indWordHandle = None
		self.dependentDataTickers = None
		self.dependentTransformations = {'None':None}

	def set_data_series_criteria(self,	periodicity=12, 
										atLeastEarly=None, 
										atLeastLate=None,
										ignoreTickers=[]):
		'''
			actually adding a list
		'''
		self.dependentDataTickers = retrieve_DataSeries_Filtered(	self.hndl_DB.cursor_(), 
																	column=TICKER,
																	minDate=atLeastEarly, 
																	maxDate=atLeastLate, 
																	periodicity=periodicity, 
																	categorical=None)
		if self.indWordHandle is not None:
			self.remove_dependent_data_series(self.indDataHandle.seriesTicker)
		for ticker in ignoreTickers:
			self.remove_dependent_data_series(ticker)

	def remove_dependent_data_series(self, ticker):
		try: 
			idx = self.dependentDataTickers.index(ticker)
			del(self.dependentDataTickers[idx])
		except ValueError:
			pass

	def set_transformation_criteria(self, 	timeChange=None,
											categorization=None):
		'''
		'''
		raise NotImplementedError

	def register_dependent_transformations(self, transList=[], includeNone=True):
		if includeNone:
			self.dependentTransformations = {'None':None}	
		else:
			self.dependentTransformations = {}
		for transformation in transList:
			assert transformation in TransformationPatterns
			self.dependentTransformations[transformation] = None

	def set_independent_data_series(self, dataHandle):
		self.indDataHandle = dataHandle
		self.remove_dependent_data_series(self.indDataHandle.seriesTicker)

	def set_independent_transformation(self, transformation='None'):
		assert transformation in TransformationPatterns
		self.indTrnsHandle = EMF_Transformation_Handle(transformation)

	def get_independent_word_handle(self):
		if self.indWordHandle is None:
			self.indWordHandle = EMF_WordSeries_Handle(self.hndl_DB, self.indDataHandle, self.indTrnsHandle)
		return self.indWordHandle

	def get_dependent_word_handles_complete_set(self):
		pass

	def get_dependent_word_handles_random_subset(self, numWords=None):
		if numWords is None:
			numWords = geometric(WORD_COUNT_GEOMETRIC_PARAM)
		count = 0
		chosen = {}
		while (len(chosen) < numWords) and (count < numWords*10):
			dataTicker = choice(self.dependentDataTickers)
			dataHandle = EMF_DataSeries_Handle(self.hndl_DB)
			dataHandle.set_data_series(ticker=dataTicker)
			trnsPattern = choice(self.dependentTransformations.keys())
			trnsHandle = EMF_Transformation_Handle(trnsPattern)
			wordName = generate_Word_Series_name(dataHandle, trnsHandle)
			if wordName in self.depWordCache:
				chosen[wordName] = self.depWordCache[wordName]
			else:
				chosen[wordName] = EMF_WordSeries_Handle(self.hndl_DB, dataHandle, trnsHandle)
				self.depWordCache[wordName] = chosen[wordName]
			count += 1 # Because I'm paranoid about infinite loops
		return chosen.values()

	# def __get_word(self, dataHandle, trnsHandle):
	# 	wordName = generate_Word_Series_name(dataHandle, trnsHandle)
	# 	if wordName in self.depWordCache:
	# 		return self.depWordCache[wordName]
	# 	else:
	# 		wordHandle = EMF_WordSeries_Handle(self.hndl_DB, dataHandle, trnsHandle)
	# 		self.depWordCache[wordName] = wordHandle
	# 		return wordHandle
