# EMF 		Import...As
import 	util_Testing 	as utl_Tst
# System 	Import...As
import 	numpy 			as np
import 	logging 		as log
# System 	From...Import
from 	string 			import join



class EMF_Model_Handle:
	def __init__(self,):
		self.respVar_Hndls = []
		self.respVar_Types = []
		self.predVar_Hndls = []
		self.predVar_Types = []
		self.sampleWeights = None
		self.predictions = None

	def __str__(self):
		predVars = [str(hndl) for hndl in self.predVar_Hndls]
		predVars = join(predVars, '|')
		respVars = [str(hndl) for hndl in self.respVar_Hndls]
		respVars = join(respVars, '|')
		return '[{0}][{1}][{2}]'.format(self.model_short_name, predVars, respVars)

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

	def add_predictor_variable(self, wordHandle):
		'''
		'''
		self.predVar_Hndls.append(wordHandle)
		self.predVar_Types.append(wordHandle.get_model_categorization())

	def clear_predictor_variable(self):
		self.predVar_Hndls = []
		self.predVar_Types = []

	def add_response_variable(self, wordHandle):
		self.respVar_Hndls.append(wordHandle)
		self.respVar_Types.append(wordHandle.get_model_categorization())

	def set_valid_dates(self, validDates):
		(self.minDate, self.maxDate) = validDates

	def _evaluate_run_readiness(self):
		'''
		TODOS:
					change from returning bool to raising value error
		'''
		if not len(self.respVar_Hndls): return False
		# for hndl_Word in self.respVar_Hndls[1:]:
		# 	if not hndl_Word.check_word_alignment(self.respVar_Hndls[0]):
		# 		return False
		if not len(self.predVar_Hndls): return False
		for type_ in self.respVar_Types:
			if type_ not in self.allowed_respVar_types: return False
		for type_ in self.predVar_Types:
			if type_ not in self.allowed_predVar_types: return False
		# for hndl_Word in self.predVar_Hndls:
		# 	if not hndl_Word.check_word_alignment(self.respVar_Hndls[0]):
		# 		return False
		return True

	def run_model(self):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		Runs the model
		TODOS:
				implement sample weights for model fits
				make fit in-sample/test out-of-sample. exposing self to bias.
				change way we assert run readiness
		'''
		# Make Sure We're Ready (Don't Love This)
		assert self._evaluate_run_readiness()
		# Create Response Variable Array
		respVarArray = None
		for varHandle in self.respVar_Hndls:
			# Store history locally for later efficiency
			varHandle.save_series_local()
			# Add history to arary
			if respVarArray is None:
				respVarArray = varHandle.get_series_values_filtered(self.minDate, self.maxDate)
			else:
				respVarArray = np.hstack((respVarArray, varHandle.get_series_values_filtered(self.minDate, self.maxDate)))
		# Create Predictor Variable Array
		predVarArray = None
		for varHandle in self.predVar_Hndls:
			if predVarArray is None:
				predVarArray = varHandle.get_series_values_filtered(self.minDate, self.maxDate)
			else:
				predVarArray = np.hstack((predVarArray, varHandle.get_series_values_filtered(self.minDate, self.maxDate)))
		# Run Model
		if self.sampleWeights is not None:
			self.model.fit(predVarArray, respVarArray, self.sampleWeights)
		else:
			self.model.fit(predVarArray, respVarArray)
		# Save Scores
		self.total_score = self.determine_accuracy(predVarArray, respVarArray)
		self.adjusted_score = self.feature_importances()*self.total_score
		self.predictions = self.model.predict(predVarArray).reshape((len(respVarArray),1))
		log.info('MODEL: %s',str(self))
		log.info('MODEL: score: {0}, dates: ({1},{2}), features: {3}'.format(self.total_score, self.minDate, self.maxDate, self.adjusted_score))
		# utl_Tst.plot_data_series(self, self.respVar_Hndls[0])
		return (self.total_score, self.predictions, self.adjusted_score)

	def determine_accuracy(self, test_predVars, test_respVars, sample_weights=None):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		Perfectly accurate is 1, perfectly inaccurate is 0
		'''
		if sample_weights is not None:
			return self.model.score(test_predVars, test_respVars, sample_weights)
		else:
			return self.model.score(test_predVars, test_respVars)

	def get_series_values(self):
		return self.predictions

	def get_series_dates(self):
		return self.respVar_Hndls[0].get_series_dates_filtered(self.minDate, self.maxDate)

	def feature_importances(self):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		sum of feature importances, must sum to 1
		'''
		return self.model.feature_importances_

	def save_model(self):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		'''
		raise NotImplementedError

	def save_model_pickle(self):
		dictObj = {
		'predictions': self.predictions,
		'total_score': self.total_score,
		}
		raise NotImplementedError

	def evaluate_model(self):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		'''
		raise NotImplementedError

	def get_save_location(self):
		raise NotImplementedError
