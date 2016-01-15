# TODO:
# 	Implement multiprocessing

# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Model 			import EMF_Model_Handle
from 	handle_Results	 		import EMF_Results_Handle
from 	handle_WordSeries 		import EMF_WordSeries_Handle
from 	handle_WordSet 			import EMF_WordSet_Handle
from 	lib_DBInstructions		import insertStat_WordStatsTable
from 	lib_Model 				import AvailableModels
from 	lib_Runner_Model		import MIN_BATCH_SIZE, MAX_BATCH_SIZE, MODEL_RETENTION_THRESHHOLD
from 	lib_Runner_Model 		import PredictorTransformationKeys, ResponseTransformationKeys
# EMF 		Import...As
import 	util_Testing 			as utl_Tst
# System 	From...Import
from 	random 					import choice, randint
# System 	Import...As
import 	logging 				as log

class EMF_Model_Runner():
	def __init__(self, DBHandle):
		self.hndl_DB = DBHandle
		self.models = []
		self.periodicity = None
		self.hndl_WordSet = EMF_WordSet_Handle(self.hndl_DB)
		self.hndl_Res = EMF_Results_Handle()

	def set_model_from_template(self, template):
		'''
		TODOS:
					How to interpolate data?
		'''
		# Set Response Ticker in WordSet
		if len(template['responseTicker']) != 1:
			raise NotImplementedError
		self.hndl_WordSet.set_resp_data_ticker(template['responseTicker'][0])
		if 'responseTrns' in template:
			self.hndl_WordSet.set_resp_trns_ptrns(template['responseTrns'])
		else:
			self.hndl_WordSet.set_resp_trns_ptrns(ResponseTransformationKeys)
		if 'responseKwargs' in template:
			self.hndl_WordSet.set_resp_trns_kwargs(template['responseKwargs'])
		if 'predictorTrns' in template:
			self.hndl_WordSet.set_pred_trns_ptrns(template['predictorTrns'])
		else:
			self.hndl_WordSet.set_pred_trns_ptrns(PredictorTransformationKeys)
		if 'predictorKwargs' in template:
			self.hndl_WordSet.set_pred_trns_kwargs(template['predictorKwargs'])

		# Set Predictor Variable(s) in WordSet
		if 'predictorCriteria' in template and len(template['predictorCriteria']):
			self.hndl_WordSet.set_predictor_data_criteria(**template['predictorCriteria'])
		# Set Models
		for model in template['models']:
			self.models.append(AvailableModels[model])

	def train_model_batch(self):
		# Choose Model at Random
		hndl_Model = choice(self.models)(self.hndl_WordSet)
		# Choose Response Word at Random
		self.hndl_WordSet.select_response_word_handle_random()
		self.hndl_Res.set_response_word(self.hndl_WordSet.respWord)
		# Run Batches
		for i in xrange(randint(MIN_BATCH_SIZE, MAX_BATCH_SIZE)):
			# Generate Words
			self.hndl_WordSet.select_predictor_word_handles_random()
			# Run Model
			hndl_Model.train_model()
			# log.info(hndl_Model.train_score) #TEST: Delete
			# log.info(hndl_Model.feature_importances()) #TEST: Delete
			# predictions = hndl_Model.get_series_values() #TEST: Delete
			# dates = hndl_Model.get_series_dates() #TEST: Delete
			self.__save_model_results(hndl_Model)
			# utl_Tst.plot_data_series(self.hndl_WordSet.get_response_word_raw(), hndl_Model)  #TEST: Delete
			# Prepare WordSet for Next Run (Not Really Nec. Safety First?)
			self.hndl_WordSet.clear_pred_word_handles()
		return self.hndl_Res

	def __save_model_results(self, hndl_Model):
		score = hndl_Model.test_model()
		if score >= MODEL_RETENTION_THRESHHOLD:
			log.info('Model accepted with score {0}'.format(score))
			self.hndl_Res.add_model(hndl_Model)
		else:
			log.info('Model rejected with score {0}'.format(score))
		# Put stats in db
		respID = self.hndl_WordSet.get_response_word_handle().wordSeriesID
		conn = self.hndl_DB.conn_()
		cursor = self.hndl_DB.cursor_()
		for (hndl_Word, score) in zip(self.hndl_WordSet.predWords, hndl_Model.adjusted_feat_scores):
			predID = hndl_Word.wordSeriesID
			insertStat_WordStatsTable(conn, cursor, respID, predID, score)
		# if bad model, register dataSeries and transformations as not-helpful
		# if good model, register dataSeries and transformations as helpful 