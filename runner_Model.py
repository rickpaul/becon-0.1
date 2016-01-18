# TODO:
# 	Implement multiprocessing

# EMF 		From...Import
from 	handle_Results	 		import EMF_Results_Handle
from 	handle_WordSelector 	import EMF_WordSelector_Handle
from 	handle_WordSet 			import EMF_WordSet_Handle
from 	lib_DBInstructions		import insertStat_WordStatsTable
from 	lib_Model 				import AvailableModels
from 	lib_Runner_Model		import MIN_BATCH_SIZE, MAX_BATCH_SIZE, MODEL_RETENTION_THRESHHOLD
from 	lib_Runner_Model 		import PredictorTransformationKeys, ResponseTransformationKeys
# EMF 		Import...As
import 	util_Testing 			as utl_Tst # Delete
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
		'''
		TODOS:
					How to interpolate data?
		'''
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
		# Choose Model at Random
		hndl_Model = choice(self.models)(self.hndl_WordSet)
		# Choose Response Word at Random
		# Add Response Word to WordSet
		self.hndl_WrdSlct.select_resp_word_random()
		self.hndl_WordSet.resp_word = self.hndl_WrdSlct.resp_word
		# Add Response Word to WordSet
		self.hndl_Res.set_response_word(self.hndl_WordSet.resp_word)
		# Run Batches
		for i in xrange(randint(MIN_BATCH_SIZE, MAX_BATCH_SIZE)):
			# Add Predictive Words to WordSet
			self.hndl_WrdSlct.select_pred_words_random()
			self.hndl_WordSet.pred_words = self.hndl_WrdSlct.pred_words
			# Run Model
			hndl_Model.train_model()
			log.info(hndl_Model.train_score) #TEST: Delete
			log.info(hndl_Model.feature_importances()) #TEST: Delete
			predictions = hndl_Model.get_series_values() #TEST: Delete
			dates = hndl_Model.get_series_dates() #TEST: Delete
			self.__save_model_results(hndl_Model)
			utl_Tst.plot_data_series(self.hndl_WordSet.resp_word.hndl_Data, hndl_Model)  #TEST: Delete
			# Prepare WordSet for Next Run (Not Really Nec. Safety First?)
			del self.hndl_WrdSlct.pred_words
			del self.hndl_WordSet.pred_words
		return self.hndl_Res

	def __save_model_results(self, hndl_Model):
		score = hndl_Model.test_model()
		if score >= MODEL_RETENTION_THRESHHOLD:
			log.info('MODEL: Model accepted with score {0}'.format(score))
			self.hndl_Res.add_model(hndl_Model)
		else:
			log.info('MODEL: Model rejected with score {0}'.format(score))
		# Put stats in db
		respID = self.hndl_WordSet.resp_word.wordSeriesID
		conn = self.hndl_DB.conn
		cursor = self.hndl_DB.cursor
		for (hndl_Word, score) in zip(self.hndl_WordSet.pred_words, hndl_Model.adjusted_feat_scores):
			predID = hndl_Word.wordSeriesID
			insertStat_WordStatsTable(conn, cursor, respID, predID, score)
		# if bad model, register dataSeries and transformations as not-helpful
		# if good model, register dataSeries and transformations as helpful 