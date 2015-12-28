# System 	Import...As
import numpy as np

class EMF_Model_Handle:
	def __init__(self,):
		self.independentVariables = []
		self.independentVariable_Types = []
		self.dependentVariables = []
		self.dependentVariable_Types = []

	def add_keyword_argument(self, kwarg, kwargValue):
		origValue = self.kwargs.get(kwarg, None)
		self.kwargs[kwarg] = kwargValue
		return origValue

	def remove_keyword_argument(self, kwarg):
		if kwarg in self.kwargs:
			origValue = self.kwargs[kwarg]
			del self.kwargs[kwarg]
			return origValue
		else:
			return None

	def add_dependent_variable(self, wordHandle, wordType):
		'''
		TODOS:
				make sure wordHandle works
		'''
		self.dependentVariables.append(wordHandle)
		self.dependentVariable_Types.append(wordType)

	def add_independent_variable(self, wordHandle, wordType):
		self.independentVariables.append(wordHandle)
		self.independentVariable_Types.append(wordType)

	def run_model(self):
		'''
		TODOS:
				implement sample weights for model fits
		'''

		assert self._evaluate_run_readiness()
		indVarArray = None
		for varHandle in self.independentVariables:
			if indVarArray is None:
				indVarArray = varHandle.get_word_series(saveHistoryLocal=True)
			else:
				indVarArray = np.hstack((indVarArray, varHandle.get_word_series()))
		depVarArray = None
		for varHandle in self.dependentVariables:
			if depVarArray is None:
				depVarArray = varHandle.get_word_series()
			else:
				depVarArray = np.hstack((depVarArray, varHandle.get_word_series()))
		self.model.fit(depVarArray, indVarArray)
		# self.model.fit(depVarArray, indVarArray, sampleWeights)

	# def get_dependent_variables(self):
	# 	raise NotImplementedError

	# def get_independent_variables(self):
	# 	raise NotImplementedError

	# def add_independent_variable_Random(self):
	# 	'''
	# 	Adds a Randomly-selected word
	# 	'''
	# 	raise NotImplementedError

	# def add_independent_variable_SemiRandom(self):
	# 	'''
	# 	Adds a Semi-Randomly-selected word based on certain criteria
	# 	'''
	# 	raise NotImplementedError

	def _evaluate_run_readiness(self):
		if not len(self.independentVariables): return False
		if not len(self.dependentVariables): return False
		for type_ in self.independentVariable_Types:
			if type_ not in self.allowed_independent_variable_types: return False
		for type_ in self.dependentVariable_Types:
			if type_ not in self.allowed_dependent_variable_types: return False
		return True