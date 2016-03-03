# TODO:
# 	Implement multiprocessing
# 	Compare Regression Coefficients (rolling basis) for __evaluate model
# 	Compare Mean Var Statistics (rolling basis) for __evaluate model
# 	Find way to compare peak/trough times for __evaluate model

# EMF 		From...Import
from 	handle_Results	 		import EMF_Results_Handle
from 	handle_WordSelector 	import EMF_WordSelector_Handle
from 	handle_WordSet 			import EMF_WordSet_Handle
from 	lib_DBInstructions		import insertStat_WordStatsTable
from 	lib_Model 				import AvailableModels
from 	lib_Runner_Model		import MIN_BATCH_SIZE, MAX_BATCH_SIZE, MODEL_RETENTION_THRESHHOLD
from 	lib_Runner_Model 		import PredictorTransformationKeys, ResponseTransformationKeys
from 	lib_Runner_Model		import TRAINING, PREDICTION_INDEPENDENT, PREDICTION_DEPENDENT
# EMF 		Import.self..As
import 	util_Runner_Model 		as utl_RnM
# System 	From...Import
from 	random 					import choice, randint
# System 	Import...As
import 	logging 				as log

class EMF_Model_Runner(object):
	def __init__(self, DBHandle):
		self.hndl_DB = DBHandle
		self.hndl_WordSet = EMF_WordSet_Handle(self.hndl_DB)
		self.hndl_WrdSlct = EMF_WordSelector_Handle(self.hndl_DB)
		self.hndl_Res = EMF_Results_Handle()
		self.models = []

	def set_model_from_template(self, template):
		# Set Response Ticker in WordSelector
		self.hndl_WrdSlct.resp_data_tickers = template['responseTicker']
		if 'responseTrns' in template:
			self.hndl_WrdSlct.resp_trns_ptrns 	= template['responseTrns']
		else:
			self.hndl_WrdSlct.resp_trns_ptrns 	= ResponseTransformationKeys
		if 'responseKwargs' in template:
			self.hndl_WrdSlct.resp_trns_kwargs 	= template['responseKwargs']
		if 'responseCanPredict' in template:
			self.hndl_WrdSlct.resp_can_predict 	= template['responseCanPredict']
		if 'predictorKwargs' in template:
			self.hndl_WrdSlct.pred_trns_kwargs 	= template['predictorKwargs']
		if 'predictorCriteria' in template:
			predCrit = template['predictorCriteria']
			if 'periodicity' in predCrit:
				self.hndl_WrdSlct.pred_data_periodicity 	= predCrit['periodicity']
			if 'categorical' in predCrit:
				self.hndl_WrdSlct.pred_data_is_categorical 	= predCrit['categorical']
			if 'minDate' in predCrit:
				self.hndl_WrdSlct.pred_data_min_date 		= predCrit['minDate']
			if 'maxDate' in predCrit:
				self.hndl_WrdSlct.pred_data_max_date 		= predCrit['maxDate']
			if 'matchRespPeriodicity' in predCrit:
				raise NotImplementedError
		if 'predictorTrns' in template:
			self.hndl_WrdSlct.pred_trns_ptrns 	= template['predictorTrns']
		else:
			self.hndl_WrdSlct.pred_trns_ptrns 	= PredictorTransformationKeys
		# Set Models
		for model in template['models']:
			self.models.append(AvailableModels[model])

	def train_model_batch(self):
		'''
		'''
		# Choose Model at Random
		self.hndl_Model = choice(self.models)(self.hndl_WordSet)
		# Choose Response Word at Random and Add Response Word to WordSet
		self.hndl_WordSet.resp_words = self.hndl_WrdSlct.select_resp_words_random()
		# Add Response Word to Result Handle
		self.hndl_Res.set_response_words(self.hndl_WordSet.resp_words)
		# Run Batches
		for i in xrange(randint(MIN_BATCH_SIZE, MAX_BATCH_SIZE)):
			# Add Predictive Words to WordSet
			# self.hndl_WordSet.pred_words = self.hndl_WrdSlct.select_pred_words_random()
			self.hndl_WordSet.pred_words = self.hndl_WrdSlct.select_pred_words_effectiveness()
			# Make Sure WordSet is Prepared
			self.__evaluate_run_readiness()
			# Run Model
			(pred_array, resp_array) = self.hndl_WordSet.get_word_arrays(mode=TRAINING, bootstrap=True)
			for (j, hndl_Word) in enumerate(self.hndl_WordSet.resp_words):
				self.hndl_Model.train_model(pred_array, resp_array[:,j])
				self.__save_model_results(hndl_Word, j)
			# Prepare Predictive Words for Next Run (Safety First)
			del self.hndl_WrdSlct.pred_words
			del self.hndl_WordSet.pred_words
		# Prepare Response Words and Model for Next Run (Safety First)
		del self.hndl_Model
		del self.hndl_WrdSlct.resp_words
		del self.hndl_WrdSlct.resp_words
		return self.hndl_Res

	def __save_model_results(self, hndl_Word, idx):
		'''
		TODO:
					Remove Spaghetti code of pushing around idx (create run_model instance)
		'''
		self.hndl_WordSet.save_predictions(self.hndl_Model, hndl_Word)
		# self.hndl_WordSet.plot_values(hndl_Word) # TEST: DELETE
		score = self.__evaluate_model(hndl_Word, idx)
		if score >= MODEL_RETENTION_THRESHHOLD:
			log.info('MODEL: Model accepted with score {0}'.format(score))
			(dates, values) = self.hndl_WordSet.get_prediction_series(hndl_Word)
			self.hndl_Res.add_model(self.hndl_Model, dates, values, score)
		else:
			log.info('MODEL: Model rejected with score {0}'.format(score))
		# Put Word Statistics In DB
		self.hndl_WrdSlct.save_word_statistics(score*self.hndl_Model.adjusted_feat_scores, hndl_Word)
		# Put Data Statistics In DB
		self.hndl_WrdSlct.save_data_statistics(score*self.hndl_Model.adjusted_feat_scores, hndl_Word)
		# Put Model Statistics In DB
		# Not Implemented

	def __evaluate_model(self, hndl_Word, idx):
		'''
		TODO:
					Remove Spaghetti code of pushing around idx (create run_model instance)
		'''
		(smoothed, pred, raw, res) = self.hndl_WordSet.get_residual_data(hndl_Word)
		(pred_array, resp_array) = self.hndl_WordSet.get_word_arrays(mode=TRAINING, bootstrap=False)
		score = self.hndl_Model.test_model(pred_array, resp_array[:,idx]) # Need this for word statistics
		# Compare Modeled Levels
		score_3 = abs(utl_RnM.level_outlier_proportion(smoothed, raw, check_fn=utl_RnM.more_than_three)-.003)
		score_2 = abs(utl_RnM.level_outlier_proportion(smoothed, raw, check_fn=utl_RnM.more_than_two)-.05)
		score_1 = abs(utl_RnM.level_outlier_proportion(smoothed, raw, check_fn=utl_RnM.more_than_one)-.32)
		score -= 2*(score_3+score_2+score_1)
		# Compare Modeled Changes
		score_3 = abs(utl_RnM.change_outlier_proportion(smoothed, raw, check_fn=utl_RnM.more_than_three)-.003)
		score_2 = abs(utl_RnM.change_outlier_proportion(smoothed, raw, check_fn=utl_RnM.more_than_two)-.05)
		score_1 = abs(utl_RnM.change_outlier_proportion(smoothed, raw, check_fn=utl_RnM.more_than_one)-.32)
		score -= 1*(score_3+score_2+score_1)
		# Prefer Smooth Model Levels
		score_3 = abs(utl_RnM.level_outlier_proportion(smoothed, pred, check_fn=utl_RnM.more_than_three)-.003)
		score_2 = abs(utl_RnM.level_outlier_proportion(smoothed, pred, check_fn=utl_RnM.more_than_two)-.05)
		score_1 = abs(utl_RnM.level_outlier_proportion(smoothed, pred, check_fn=utl_RnM.more_than_one)-.32)
		score -= .3*(score_3+score_2+score_1)
		# Prefer Smooth Model Changes
		score_3 = abs(utl_RnM.level_outlier_proportion(smoothed, pred, check_fn=utl_RnM.more_than_three)-.003)
		score_2 = abs(utl_RnM.level_outlier_proportion(smoothed, pred, check_fn=utl_RnM.more_than_two)-.05)
		score_1 = abs(utl_RnM.level_outlier_proportion(smoothed, pred, check_fn=utl_RnM.more_than_one)-.32)
		score -= .7*(score_3+score_2+score_1)
		return score

	def __evaluate_run_readiness(self):
		'''
		TODOS:
					is this even necessary?
		'''
		if not self.hndl_WordSet.predictor_words_are_set(): 
			raise AttributeError
		if not self.hndl_WordSet.response_word_is_set():
			raise AttributeError
		for type_ in self.hndl_WordSet.get_response_word_types():
			if type_ not in self.hndl_Model.allowed_respVar_types:
				raise AttributeError
		for type_ in self.hndl_WordSet.get_predictor_word_types():
			if type_ not in self.hndl_Model.allowed_predVar_types:
				raise AttributeError


