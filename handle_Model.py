# System 	Import...As
import numpy as np

class EMF_Model_Handle:
	def __init__(self,):
		self.indVar_Hndls = []
		self.indVar_Types = []
		self.depVar_Hndls = []
		self.depVar_Types = []
		self.sampleWeights = None

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

	def add_dependent_variable(self, wordHandle):
		'''
		TODOS:
				make sure wordHandle works
		'''
		self.depVar_Hndls.append(wordHandle)
		self.depVar_Types.append(wordHandle.get_model_categorization())

	def clear_dependent_variables(self):
		self.depVar_Hndls = []
		self.depVar_Types = []

	def add_independent_variable(self, wordHandle):
		self.indVar_Hndls.append(wordHandle)
		self.indVar_Types.append(wordHandle.get_model_categorization())

	def _evaluate_run_readiness(self):
		if not len(self.indVar_Hndls): return False
		if not len(self.depVar_Hndls): return False
		for type_ in self.indVar_Types:
			if type_ not in self.allowed_indVar_types: return False
		for type_ in self.depVar_Types:
			if type_ not in self.allowed_depVar_types: return False
		return True

	def run_model(self):
		'''
		FROM MODEL TEMPLATE
		Runs the model
		TODOS:
				implement sample weights for model fits
				make fit in-sample/test out-of-sample. exposing self to bias.
				change way we assert run readiness
		'''
		# Make Sure We're Ready (Don't Love This)
		assert self._evaluate_run_readiness()
		# Create Dependent Variable Array
		indVarArray = None
		for varHandle in self.indVar_Hndls:
			if indVarArray is None:
				indVarArray = varHandle.get_word_series(saveHistoryLocal=True)
			else:
				indVarArray = np.hstack((indVarArray, varHandle.get_word_series()))
		# Create Dependent Variable Array
		depVarArray = None
		for varHandle in self.depVar_Hndls:
			if depVarArray is None:
				depVarArray = varHandle.get_word_series()
			else:
				depVarArray = np.hstack((depVarArray, varHandle.get_word_series()))
		# Run the model
		if self.sampleWeights is not None:
			self.model.fit(depVarArray, indVarArray, self.sampleWeights)
		else:
			self.model.fit(depVarArray, indVarArray)
		# Save the Scores
		self.total_score = self.determine_accuracy(depVarArray, indVarArray)
		self.adjusted_score = self.feature_importances()*self.total_score
		self.predictions = self.model.predict(depVarArray).reshape((len(indVarArray),1))
		return (self.total_score, self.predictions, self.adjusted_score)

	def determine_accuracy(self, test_depVars, test_indVars, sample_weights=None):
		'''
		FROM MODEL TEMPLATE
		Perfectly accurate is 1, perfectly inaccurate is 0
		(This Gives Percent Matching Prediction)
		'''
		if sample_weights is not None:
			return self.model.score(test_depVars, test_indVars, sample_weights)
		else:
			return self.model.score(test_depVars, test_indVars)

	def feature_importances(self):
		'''
		FROM MODEL TEMPLATE
		sum of feature importances, must sum to 1
		'''
		return self.model.feature_importances_

	def save_model(self):
		raise NotImplementedError

	def evaluate_model(self):
		raise NotImplementedError
