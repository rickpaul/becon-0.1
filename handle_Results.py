# EMF 		From...Import
from 	handle_ColumnArray 		import EMF_ColumnArray_Handle
from 	lib_JSON 				import JSON_MODEL_ID, JSON_MODEL_CONFIDENCE
from 	lib_JSON 				import JSON_MODEL_DESC, JSON_MODEL_CATS
from 	lib_Runner_Model 		import MODEL_SCORE
from 	util_Results			import get_prediction_array_path, get_results_metadata_path
from 	util_WordSeries 		import raw_word_key
# System	From...Import
from 	string 					import join
# System 	Import...As
import 	logging 				as log
import 	numpy	 				as np
import 	pandas	 				as pd


class EMF_Results_Handle(EMF_ColumnArray_Handle):
	def __init__(self):
		self._resp_words = None
		#
		self._file_name = None
		self._array_file_path = None
		self._metadata_file_path = None
		#
		self._log_prefix = 'RESULTS'
		super(EMF_Results_Handle, self).__init__(save_to_file=True)
		self.max_size = 100

	def log_prefix():
		doc = ""
		def fget(self):
			return self._log_prefix
		return locals()
	log_prefix = property(**log_prefix())

	def file_name():
		doc = ""
		def fget(self):
			if self._file_name is None:
				name_arr = sorted([w.data_ticker for w in self._resp_words])
				self._file_name = join(name_arr, '|')
			return self._file_name
		def fdel(self):
			self._file_name = None
		return locals()
	file_name = property(**file_name())

	def metadata_file_path():
		doc = ""
		def fget(self):
			if self._metadata_file_path is None:
				self._metadata_file_path = get_results_metadata_path(self.file_name)
			return self._metadata_file_path
		return locals()
	metadata_file_path = property(**metadata_file_path())

	def array_file_path():
		doc = ""
		def fget(self):
			if self._array_file_path is None:
				self._array_file_path = get_prediction_array_path(self.file_name)
			return self._array_file_path
		return locals()
	array_file_path = property(**array_file_path())

	# def model_info():
	# 	doc = "The model_info property."
	# 	def fget(self):
	# 		return self._col_metadata
	# 	def fset(self, value):
	# 		self._col_metadata = value
	# 	return locals()
	# model_info = property(**model_info())

	def get_resp_word_raw_values(self, hndl_Word=None):
		if hndl_Word == None:
			if len(self._resp_words) != 1:
				raise NameError
			else:
				hndl_Word = self._resp_words[0]
		key_ = raw_word_key(hndl_Word)
		return self.get_values_by_col(key_, filter_nulls=True)

	def get_prediction_dates(self):
		keys = [raw_word_key(w) for w in self._resp_words]
		filter_ = self.col_array[keys[0]].isnull()
		for i in xrange(1, len(keys)):
			filter_ = filter_ | self.col_array[keys[1]].isnull()
		return np.array(self.col_array[filter_].index)

	def delete_models(self):
		'''
		TODO:
					Make more efficient: store minimum score?
					Move to ColumnArray?
		'''
		curr_size = self.col_array.shape[1]
		oversize = curr_size - self.max_size
		if oversize > 0:
			log.info('RESULTS: Current Predictions have {0} too many models'.format(oversize))
			delete_scores = sorted(self.col_metadata.items(), key=lambda a: a[1][MODEL_SCORE]) #sorts ascending
			delete_keys = map(lambda a: a[0], delete_scores[:oversize])
			for key_ in delete_keys:
				log.info('RESULTS: Deleting Model #{0}'.format(key_))
				del self.col_metadata[str(key_)]
				del self.col_array[str(key_)]
		else:
			log.info('RESULTS: Predictions Array has {0} models. Max is '.format(curr_size, self.max_size))

	def add_model(self, hndl_Model, dates, values, model_score):
		assert self._resp_words is not None
		self.add_column(dates, values)
		self.__add_model_metadata(hndl_Model, model_score)
		self.col_index += 1
		self.delete_models()
		self.save()	

	def get_model_metadata(self, model_idx):
		return self.col_metadata[str(model_idx)]

	def __add_model_metadata(self, hndl_Model, model_score):
		'''
		TODO:
				By accepting score from evaluate model, we're preferring more conservative models 
					(i.e. something that predicts out 24 won't be accepted most likely.)
					How can we sort on two dimensions?
					Should we move __evaluate_model from runner_Model to here?
		'''
		# model_name = str(hndl_Model)
		# self._model_scores.append((self.model_index, model_score))
		model_acc = hndl_Model.test_score
		model_desc = hndl_Model.cat_desc
		model_categories = hndl_Model.category_importances
		# model_start	
		# model_end		
		self.add_metadata({
			MODEL_SCORE: 			model_score,
			JSON_MODEL_ID :			self.col_index, 
			JSON_MODEL_CONFIDENCE :	model_acc, 
			JSON_MODEL_DESC :		model_desc,
			JSON_MODEL_CATS : 		model_categories
		}, key=self.col_index)

	def set_response_words(self, respWords, refillResp=False):
		self._resp_words = respWords
		keys = [str(w) for w in self._resp_words]
		log.info('RESULTS: Setting Results Response Words: {0}'.format(keys))
		# Load Data if Saved
		self.load()
		for hndl_Word in self._resp_words:
			key = raw_word_key(hndl_Word)
			self.add_column(hndl_Word.get_raw_dates(), hndl_Word.get_raw_values(), key=key, force=refillResp)

	# def get_prediction_values(self, index):
	# 	row = self.col_array.ix[index]
	# 	row_filter = ~row.isnull()
	# 	pred_values = row[row_filter]
	# 	model_idxs = np.array(pred_values.index)
	# 	pred_values = np.array(pred_values)
	# 	return (model_idxs, pred_values)

	# def get_rawVal_latest_date(self):
	# 	return max(self.predictionArray[~self.predictionArray[0].isnull()].index)

	# def get_latest_date(self):
	# 	return max(self.predictionArray.index)

	# def get_earliest_date(self):
	# 	return min(self.predictionArray.index)

	# def get_predictions_filtered(self, min_, max_):
	# 	return self.predictionArray[self.predictionArray.index>=min_ & self.predictionArray.index<=max_]
