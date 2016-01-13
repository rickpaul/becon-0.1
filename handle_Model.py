# EMF 		Import...As
from 	lib_Runner_Model		import TRAINING, PREDICTION
from 	template_SerialHandle 	import EMF_Serial_Handle
# System 	Import...As
import 	numpy 					as np
import 	logging 				as log
# System 	From...Import
from 	string 					import join



class EMF_Model_Handle(EMF_Serial_Handle):
	def __init__(self, hndl_WordSet):
		self.hndl_WordSet = hndl_WordSet

	def __str__(self):
		return self.model_short_name
		predVars = [str(hndl) for hndl in [self.hndl_WordSet.respWord]]
		predVars = join(predVars, '|')
		respVars = [str(hndl) for hndl in self.hndl_WordSet.predWords]
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

	def _evaluate_run_readiness(self):
		'''
		TODOS:
					change from returning bool to raising value error
		'''
		if not self.hndl_WordSet.predictor_words_are_set(): return False
		if not self.hndl_WordSet.response_word_is_set(): return False
		for type_ in [self.hndl_WordSet.get_response_word_type()]:
			if type_ not in self.allowed_respVar_types: return False
		for type_ in self.hndl_WordSet.get_predictor_word_types():
			if type_ not in self.allowed_predVar_types: return False
		return True

	def train_model(self):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		Runs the model
		TODOS:
				implement sample weights for model fits
				make fit in-sample/test out-of-sample. Curr. exposing self to bias.
				change way we assert run readiness
		'''
		# Make Sure We're Ready (Don't Love This)
		assert self._evaluate_run_readiness()
		(predVarArray, respVarArray) = self.hndl_WordSet.get_word_arrays(mode=TRAINING, bootstrap=True)
		# Run Model
		if self.hndl_WordSet.sampleWeights is not None:
			self.model.fit(predVarArray, respVarArray, self.hndl_WordSet.sampleWeights)
		else:
			self.model.fit(predVarArray, respVarArray)
		# Save Scores
		self.train_score = self.determine_accuracy(predVarArray, respVarArray)
		self.adjusted_feat_scores = self.feature_importances()*self.train_score

	def test_model(self):
		(predVarArray, respVarArray) = self.hndl_WordSet.get_word_arrays(mode=TRAINING, bootstrap=True)
		self.test_score = self.determine_accuracy(predVarArray, respVarArray)
		self.adjusted_feat_scores = self.feature_importances()*self.test_score
		return self.test_score

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
		predictions = self.model.predict(self.hndl_WordSet.get_word_arrays(mode=PREDICTION)[0])
		predictions = predictions.reshape((len(predictions), 1))
		return self.hndl_WordSet.get_predicted_values(predictions=predictions)

	def get_series_dates(self):
		return self.hndl_WordSet.get_predicted_dates()

	def feature_names(self):
		return self.hndl_WordSet.features

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

	# def save_model_pickle(self):
	# 	dictObj = {
	# 	'predictions': self.predictions,
	# 	'total_score': self.total_score,
	# 	}
	# 	raise NotImplementedError

	def evaluate_model(self):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		'''
		raise NotImplementedError

	def get_save_location(self):
		raise NotImplementedError
