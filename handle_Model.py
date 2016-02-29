# TODO:
# 	Remove WordSet from this.
# 	Reduce Template Necessities
# 	Make Dependency on Template
# 	Figure out why I can't get NotFittedError
# 	Figure out where we planned on using data_importances, or remove

# EMF 		Import...As
from 	lib_Runner_Model		import TRAINING, PREDICTION_DEPENDENT, PREDICTION_INDEPENDENT
# from 	template_SerialHandle 	import EMF_Serial_Handle
# System 	Import...As
import 	numpy 					as np
import 	logging 				as log
# System 	From...Import
from 	string 					import join
# from 	sklearn.exceptions 		import NotFittedError

FEAT_IMP_MIN = 0.005 # Importance at which model decides not to describe (50bps)

class EMF_Model_Handle(object):

	def __init__(self, hndl_WordSet):
		self.hndl_WordSet = hndl_WordSet
		# self._predictions = None
		self._test_score = None
		self._train_score = None

	def __str__(self):
		respVars = [str(hndl) for hndl in self.hndl_WordSet.resp_words]
		respVars = join(respVars, '|')
		predVars = [str(hndl) for hndl in self.hndl_WordSet.pred_words]
		predVars = join(predVars, '|')
		return '[{0}][{1}][{2}]'.format(self.model_short_name, respVars, predVars)

	def desc():
		'''
		A more descriptive string
		Probably should be overwritten by sub-modules
		'''
		def fget(self):
			resp_desc = [hndl.desc for hndl in self.hndl_WordSet.resp_words]
			if len(resp_desc) > 2:
				resp_desc = join(resp_desc[:-1], ', ') + ', and ' + resp_desc[-1]
			elif len(resp_desc) == 2:
				resp_desc = '{0} and {1}'.format(resp_desc[0], resp_desc[1])
			else:
				resp_desc = resp_desc[0]
			feature_importances = self.feature_importances
			if feature_importances is not None:
				pred_desc = []
				for (feat_imp, hndl) in zip(feature_importances, self.hndl_WordSet.pred_words):
					if feat_imp > 0:
						pred_desc.append(hndl.desc)
			else:
				pred_desc = [hndl.desc for hndl in self.hndl_WordSet.pred_words]
			if len(pred_desc) > 2:
				pred_desc = join(pred_desc[:-1], ', ') + ', and ' + pred_desc[-1]
				return 'The {0} together describe the {1}'.format(pred_desc, resp_desc)
			elif len(pred_desc) == 2:
				return 'The {0} and {1} describe the {2}'.format(pred_desc[0], pred_desc[1], resp_desc)
			else:
				return 'The {0} describes the {1}'.format(pred_desc, resp_desc)
		return locals()
	desc = property(**desc())

	def cat_desc():
		def fget(self):
			# Get Response Description
			resp_desc = [hndl.desc for hndl in self.hndl_WordSet.resp_words]
			if len(resp_desc) > 2:
				resp_desc = join(resp_desc[:-1], ', ') + ', and ' + resp_desc[-1]
			elif len(resp_desc) == 2:
				resp_desc = '{0} and {1}'.format(resp_desc[0], resp_desc[1])
			else:
				resp_desc = resp_desc[0]
			# Get Predictor Description
			pred_desc = []
			for (key, val) in self.category_importances.iteritems():
				pred_desc.append(key + ' ({0:.1f}%)'.format(val*100))
			if len(pred_desc) > 2:
				pred_desc = join(pred_desc[:-1], ', ') + ', and ' + pred_desc[-1]
				return '{0} together describe the {1}'.format(pred_desc, resp_desc)
			elif len(pred_desc) == 2:
				return '{0} and {1} describe the {2}'.format(pred_desc[0], pred_desc[1], resp_desc)
			else:
				return '{0} describes the {1}'.format(pred_desc, resp_desc)
		return locals()
	cat_desc = property(**cat_desc())

	def feature_importances():
		doc = "The feature_importances property."
		def fget(self):
			try:
				return self.model.feature_importances_
			# except NotFittedError:
			except Exception:
				log.warning('MODEL: No Feature Importances Found.')
				len_ = len(self.hndl_WordSet.pred_words)
				return np.ones(len_)/(len_*1.0)
		return locals()
	feature_importances = property(**feature_importances())

	def category_importances():
		doc = "The category_importances property."
		def fget(self):
			cat_imp = {}
			for (feat_imp, hndl_Word) in zip(self.feature_importances, self.hndl_WordSet.pred_words):
				if feat_imp > FEAT_IMP_MIN:
					cat_imp[hndl_Word.category] = cat_imp.get(hndl_Word.category, 0.0) + feat_imp
			return cat_imp
		return locals()
	category_importances = property(**category_importances())

	def category_desc_importances():
		doc = "The category_desc_importances property."
		def fget(self):
			cat_imp = {}
			for (feat_imp, hndl_Word) in zip(self.feature_importances, self.hndl_WordSet.pred_words):
				if feat_imp > FEAT_IMP_MIN:
					cat_imp[hndl_Word.cat_desc] = cat_imp.get(hndl_Word.cat_desc,0.0) + feat_imp
			return cat_imp
		return locals()
	category_desc_importances = property(**category_desc_importances())

	# This is not used
	def data_importances():
		doc = "The data_importances property."
		def fget(self):
			data_imp = {}
			for (feat_imp, hndl_Word) in zip(self.feature_importances, self.hndl_WordSet.pred_words):
				dataID = hndl_Word.dataSet.seriesID
				if feat_imp > 0:
					data_imp[dataID] = data_imp.get(dataID,0.0) + feat_imp
			return data_imp
		return locals()
	data_importances = property(**data_importances())

	def train_score():
		doc = "The train_score property."
		def fget(self):
			return self._train_score
		def fset(self, value):
			self._train_score = value
		def fdel(self):
			del self._train_score
		return locals()
	train_score = property(**train_score())

	def test_score():
		doc = "The test_score property."
		def fget(self):
			if self._test_score is None:
				self.test_model()
			return self._test_score
		def fset(self, value):
			self._test_score = value
		def fdel(self):
			del self._test_score
		return locals()
	test_score = property(**test_score())

	def train_model(self, pred_array, resp_array, sample_weights=None):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		Runs the model
		TODOS:
				implement sample weights for model fits
				change way we assert run readiness
				assert minDate<maxDate
		'''
		# Run Model
		if sample_weights is not None:
			self.model.fit(pred_array, resp_array, sample_weights)
		else:
			self.model.fit(pred_array, resp_array)
		# Save Scores
		self.train_score = self.determine_accuracy(pred_array, resp_array)
		self.adjusted_feat_scores = self.feature_importances*self.train_score

	def test_model(self, pred_array, resp_array, sample_weights=None):
		self.test_score = self.determine_accuracy(pred_array, resp_array, sample_weights=sample_weights)
		self.adjusted_feat_scores = self.feature_importances*self.test_score
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

	# def feature_names(self):
	# 	return self.hndl_WordSet.features

	def save_model(self):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		This will, e.g. save tree in separable form (for description)
		'''
		raise NotImplementedError

	def model_stats(self):
		'''
		IMPLEMENTATION OF MODEL TEMPLATE
		'''
		raise NotImplementedError
		# FoD = np.ediff1d(self.predictions)
		# # Count number of single values (denotes spikes, unrealistic)
		# eq_neg_ = lambda x, y: (x==-y) and (x!=0)
		# numSpikes = sum(map(eq_neg_, FoD[1:],FoD[:-1]))
		# spike_prop = 1 - numSpikes/(len(self.predictions)-2.0)
		# Get Moment Stats


	def get_save_location(self):
		raise NotImplementedError



	# def predictions():
	# 	doc = "Predictions."
	# 	def fget(self):
	# 		predictions = self.model.predict(self.hndl_WordSet.get_word_arrays(mode=PREDICTION)[0])
	# 		predictions = predictions.reshape(-1, 1)
	# 		self._predictions = self.hndl_WordSet.get_prediction_values(predictions=predictions)
	# 		return self._predictions
	# 	return locals()
	# predictions = property(**predictions())

	# def add_keyword_argument(self, kwarg, kwargValue):
	# 	origValue = self.kwargs.get(kwarg, None)
	# 	self.kwargs[kwarg] = kwargValue
	# 	return origValue

	# def remove_keyword_argument(self, kwarg):
	# 	if kwarg in self.kwargs:
	# 		origValue = self.kwargs[kwarg]
	# 		del self.kwargs[kwarg]
	# 		return origValue
	# 	else:
	# 		return None


