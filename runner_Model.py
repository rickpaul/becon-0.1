# TODO:
# 	Implement multiprocessing

# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Model 			import EMF_Model_Handle
from 	handle_Results	 		import EMF_Results_Handle
# from 	handle_Transformation	import EMF_Transformation_Handle
from 	handle_WordSeries 		import EMF_WordSeries_Handle
from 	handle_WordSet 			import EMF_WordSet_Handle
from 	lib_DBInstructions		import insertStat_WordStatsTable
from 	lib_Model 				import AvailableModels
from 	lib_Runner_Model		import MIN_BATCH_SIZE, MAX_BATCH_SIZE, MODEL_RETENTION_THRESHHOLD
from 	lib_Runner_Model 		import PredictorTransformationKeys, ResponseTransformationKeys
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

	# DEPRECATED
	# def register_models(self, modelName=None):
	# 	if modelName is None:
	# 		self.models = AvailableModels
	# 	else:
	# 		self.models.append(AvailableModels[modelName])

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
		if len(template['dataSeriesCriteria']):
			self.hndl_WordSet.set_predictor_data_criteria(**template['dataSeriesCriteria'])
		# Set Models
		for model in template['models']:
			self.models.append(AvailableModels[model])

	def run_model_batch(self):
		# Choose Model at random
		hndl_Model = choice(self.models)()
		resp_Word = self.hndl_WordSet.get_response_word_handle_random()
		hndl_Model.add_response_variable(resp_Word)
		# Run Batches
		for i in xrange(randint(MIN_BATCH_SIZE, MAX_BATCH_SIZE)):
			# Generate Words
			pred_Words = self.hndl_WordSet.get_predictor_word_handles_random_subset()
			validDates = self.hndl_WordSet.get_word_date_range()
			self.__iterate(hndl_Model, pred_Words, resp_Word, validDates)

	def __iterate(self, model, pred_Words, resp_Word, validDates):
		for hndl_Word in pred_Words:
			model.add_predictor_variable(hndl_Word)
		model.set_valid_dates(validDates)
		# Run Model
		(score, predictions, varScores) = model.run_model()
		# Put stats in db (if score meets threshhold)
		respID = self.hndl_WordSet.get_response_word_handle_current().wordSeriesID
		conn = self.hndl_DB.conn_()
		cursor = self.hndl_DB.cursor_()
		for (hndl_Word, imp) in zip(pred_Words, varScores):
			predID = hndl_Word.wordSeriesID
			insertStat_WordStatsTable(conn, cursor, respID, predID, imp)
		# Put Predictions in Array (if score meets threshhold)
		if score >= MODEL_RETENTION_THRESHHOLD:
			log.info('Model accepted with score {0}'.format(score))
			# self.hndl_Res.add_model(model)
		else:
			log.info('Model rejected with score {0}'.format(score))
		# Prepare Model for Next Run
		model.clear_predictor_variable()

	def __assess_model(self):
		raise NotImplementedError
		# if bad model, register dataSeries and transformations as not-helpful

		# if good model, register dataSeries and transformations as helpful 
		# if good model, store feature-importances