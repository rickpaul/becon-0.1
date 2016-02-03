# EMF 		From...Import
from 	lib_JSON 		import JSON_MODEL_ID, JSON_MODEL_CONFIDENCE
from 	lib_JSON 		import 	JSON_MODEL_DESC, JSON_MODEL_CATS
from 	util_Results	import get_prediction_array_path, get_results_metadata_path
from 	util_JSON 		import save_to_JSON, load_from_JSON
# EMF 		Import...As
# System 	Import...As
import 	logging 		as log
import 	numpy	 		as np
import 	pandas	 		as pd
import 	pickle


class EMF_Results_Handle(object):
	def __init__(self):
		self.model_info = {}
		# self.predictionFeatures = {}
		self._resp_word = None
		self.dataName = None
		self.model_index = 1
		self.predictionArray = None # Panda Array of size (dates)x(models)
		self._model_scores = []
		self._max_size = 100

	def max_size():
		doc = "The max_size property."
		def fget(self):
			return self._max_size
		def fset(self, value):
			self._max_size = value
		return locals()
	max_size = property(**max_size())

	def model_info():
		doc = "The model_info property."
		def fget(self):
			return self._model_info
		def fset(self, value):
			self._model_info = value
		return locals()
	model_info = property(**model_info())

	def __del__(self):
		self.save_prediction_array_Pickle()
		self.save_metadata_json()

	def get_rawVal_basis(self):
		filtered = self.predictionArray[~self.predictionArray[0].isnull()]
		dates = np.array(filtered.index)
		values = np.array(filtered[0])
		return (dates, values)

	# def get_rawVal_latest_date(self):
	# 	return max(self.predictionArray[~self.predictionArray[0].isnull()].index)

	# def get_latest_date(self):
	# 	return max(self.predictionArray.index)

	# def get_earliest_date(self):
	# 	return min(self.predictionArray.index)

	# def get_predictions_filtered(self, min_, max_):
	# 	return self.predictionArray[self.predictionArray.index>=min_ & self.predictionArray.index<=max_]

	def get_prediction_dates(self):
		return np.array(self.predictionArray[self.predictionArray[0].isnull()].index)

	def get_prediction_values(self, index):
		row = self.predictionArray.ix[index]
		row_filter = ~row.isnull()
		pred_values = row[row_filter]
		model_idxs = np.array(pred_values.index)
		pred_values = np.array(pred_values)
		return (model_idxs, pred_values)

	def delete_models(self):
		curr_size = self.predictionArray.shape[1]
		oversize = curr_size - self.max_size
		if oversize > 0:
			log.info('RESULTS: Current Predictions have {0} too many models'.format(oversize))
			delete_scores = sorted(x, key=lambda a: a[1]) #sorts ascending
			delete_keys = map(lambda a: a[0], delete_scores[:oversize])
			for key_ in delete_keys:
				log.info('RESULTS: Deleting Model #{0}'.format(key_))
				del self.model_info[key_]
			self._model_scores = delete_scores[oversize:]
		else:
			log.info('RESULTS: Predictions Array has {0} models. Max is '.format(curr_size, self.max_size))

	def add_model(self, hndl_Model, dates, values, model_score):
		assert self._resp_word is not None
		self.__add_predictions(dates, values)
		self.__add_model_metadata(hndl_Model, model_score)
		self.model_index += 1
		self.delete_models()
		self.save_prediction_array_Pickle()
		self.save_metadata_json()		

	def get_model_metadata(self, model_idx):
		return self.model_info[model_idx]

	def __add_model_metadata(self, hndl_Model, model_score):
		'''
		TODO:
				By accepting score from evaluate model, we're preferring more conservative models 
					(i.e. something that predicts out 24 won't be accepted most likely.)
					How can we sort on two dimensions?
					Should we move __evaluate_model from runner_Model to here?
		'''
		# model_name = str(hndl_Model)
		self._model_scores.append((self.model_index, model_score))
		model_acc = hndl_Model.test_score
		model_desc = hndl_Model.cat_desc
		model_categories = hndl_Model.category_importances
		# model_start	
		# model_end		
		self.model_info[self.model_index] = {
			JSON_MODEL_ID :			self.model_index, 
			JSON_MODEL_CONFIDENCE :	model_acc, 
			JSON_MODEL_DESC :		model_desc,
			JSON_MODEL_CATS : 		model_categories
		}

	def __add_predictions(self, dates, values):
		newValues = pd.DataFrame({self.model_index: values.ravel()}, index=dates.ravel())
		self.predictionArray = pd.concat([self.predictionArray, newValues], axis=1, ignore_index=False)

	def set_response_word(self, respWord, refillResp=False):
		log.info('RESULTS: Setting Results Response Word: {0}'.format(respWord))
		self._resp_word = respWord
		self.dataName = str(respWord.hndl_Data)
		# Load Results Model State
		self.load_metadata_json()
		# Load Predictions Array
		self.load_prediction_array_Pickle()
		# Load Word History
		if self.predictionArray is None:
			log.info('RESULTS: Creating Results Prediction Array with Response Word: {0}'.format(respWord))
			values = respWord.get_raw_values()
			dates = respWord.get_raw_dates()
			self.predictionArray = pd.DataFrame({0: values.ravel()}, index=dates.ravel())
		elif refillResp:
			log.info('RESULTS: Resetting Prediction Array with Response Word: {0}'.format(respWord))
			values = respWord.get_raw_values()
			dates = respWord.get_raw_dates()
			newValues = pd.DataFrame({0: values.ravel()}, index=dates.ravel())
			self.predictionArray[0] = newValues

	def load_metadata_json(self):
		try:
			filePath = get_results_metadata_path(self.dataName)
			log.info('RESULTS: Loading Results Handle Metadata.')
			self.__dict__.update(load_from_JSON(filePath))
		except Exception, e:
			log.warning('RESULTS: Failed to Load Results Handle Metadata.')
			log.warning(e)
			log.warning('RESULTS: File path was: {0}'.format(filePath))

	def load_prediction_array_Pickle(self):
		filePath = get_prediction_array_path(self.dataName)
		try:
			log.info('RESULTS: Loading Results Handle Predictions Array.')
			self.predictionArray = pickle.load( open( filePath, "rb" ) )
			if self.predictionArray is not None:
				log.warning('RESULTS: Loading over an existing results array.')
		except Exception, e:
			log.warning('RESULTS: Failed to load results pickle.')
			log.warning(e)
			log.warning('RESULTS: File path was: {0}'.format(filePath))

	def save_metadata_json(self):
		try:
			json_ = {
				'model_index' 	: self.model_index,
				'model_info'	: self.model_info
			}
			filePath = get_results_metadata_path(self.dataName)
			log.info('RESULTS: Saving Results Handle Metadata to {0}'.format(filePath))
			save_to_JSON(filePath, json_)
		except Exception, e:
			log.warning('RESULTS: Failed to save Results Handle Metadata.')
			log.warning(e)
			log.warning('RESULTS: File path was: {0}'.format(filePath))

	def save_prediction_array_Pickle(self):
		filePath = get_prediction_array_path(self.dataName)
		try:
			log.info('RESULTS: Saving prediction array pickle to {0}'.format(filePath))
			self.predictionArray.to_pickle(filePath)
		except Exception, e:
			log.warning('RESULTS: Failed to save Predictions Array.')
			log.warning(e)
			log.warning('RESULTS: File path was: {0}'.format(filePath))

