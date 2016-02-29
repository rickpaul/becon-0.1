# TODO:
#	Remove hndl_DB?
# 	Make play nicer with timeseries 

# EMF 		From...Import
from 	handle_ColumnArray 		import EMF_ColumnArray_Handle
from 	handle_TimeSet 			import max_time_handle_merge, min_time_handle_merge
from 	lib_Runner_Model		import BOOTSTRAP_MULTIPLIER
from 	lib_Runner_Model		import TRAINING, PREDICTION_INDEPENDENT, PREDICTION_DEPENDENT
from 	util_Algorithms 		import savitzky_golay
from 	util_WordSeries 		import raw_word_key, prd_word_key, word_key
# EMF 		Import...As
# System 	Import...As
import 	numpy 					as np
import 	logging 				as log
import 	pandas	 				as pd
# System 	From...Import
from 	numpy.random 			import geometric
from 	random 					import choice

class EMF_WordSet_Handle(EMF_ColumnArray_Handle):
	def __init__(self, hndl_DB):
		self._hndl_DB = hndl_DB
		#
		self._sample_weights = None
		self._resp_words = None
		self._pred_words = None
		# self._periodicity = None
		#
		self._log_prefix = 'WORDSET'
		self.max_size=100
		super(EMF_WordSet_Handle, self).__init__(save_to_file=False)

	def log_prefix():
		doc = ""
		def fget(self):
			return self._log_prefix
		return locals()
	log_prefix = property(**log_prefix())

	def sample_weights():
		doc = "The Sample Weights."
		def fget(self):
			return self._sample_weights
		def fset(self, value):
			self._sample_weights = value
		def fdel(self):
			del self._sample_weights
		return locals()
	sample_weights = property(**sample_weights())

	def resp_words():
		doc = "The Response Word."
		def fget(self):
			return self._resp_words
		def fset(self, value):
			self._resp_words = value
			for hndl_Word in self._resp_words:
				# Add Raw Values
				dates = hndl_Word.get_raw_dates()
				values = hndl_Word.get_raw_values()
				raw_key = raw_word_key(hndl_Word)
				self.add_column(dates, values, key=raw_key, force=False)
				# Add Transformed Values
				dates = hndl_Word.get_series_dates()
				values = hndl_Word.get_series_values()
				key_ = word_key(hndl_Word)
				self.add_column(dates, values, key=key_, force=True)
		def fdel(self):
			log.info('WORDSET: Removing Response Words')
			keys = [word_key(w) for w in self._resp_words]
			keys += [raw_word_key(w) for w in self._resp_words]
			keys += [prd_word_key(w) for w in self._resp_words]
			del self._resp_words
			for key_ in keys:
				self.delete_column(key_, expect_metadata=False)
		return locals()
	resp_words = property(**resp_words())

	def pred_words():
		doc = "The Predictive Words."
		def fget(self):
			return self._pred_words
		def fset(self, value):
			self._pred_words = value
			for hndl_Word in self._pred_words:
				dates = hndl_Word.get_series_dates()
				values = hndl_Word.get_series_values()
				key_ = word_key(hndl_Word)
				self.add_column(dates, values, key=key_, force=False)
		def fdel(self):
			log.info('WORDSET: Removing Predictive Words')
			keys = [word_key(w) for w in self._pred_words]
			log.info('WORDSET: Removing Response Prediction Words (because Predictors are Removed)')
			keys += [prd_word_key(w) for w in self._resp_words]
			for key_ in keys:
				self.delete_column(key_, expect_metadata=False)
			del self._pred_words
		return locals()
	pred_words = property(**pred_words())

	def get_model_filter(self, mode=TRAINING):
		if mode == PREDICTION_INDEPENDENT:
			keys = [word_key(w) for w in self._pred_words]
		elif mode == PREDICTION_DEPENDENT:
			keys = [word_key(w) for w in self._pred_words]
			keys += [raw_word_key(w) for w in self._resp_words]
		elif mode == TRAINING:
			keys = [word_key(w) for w in self._pred_words]
			keys += [word_key(w) for w in self._resp_words]
		else:
			raise NameError
		and_ = lambda c1, c2: c1 & c2
		return reduce(and_, [~self.col_array[key].isnull() for key in keys])

	def get_word_arrays(self, mode=TRAINING, bootstrap=False):
		filter_ = self.get_model_filter(mode=mode)
		# Create Predictor Variable Array
		pred_array = None
		for hndl_Word in self._pred_words:
			new_array = self.get_values_by_col_filtered(word_key(hndl_Word), filter_, values_only=True).reshape(-1,1)
			if pred_array is None:
				pred_array = new_array
			else:
				pred_array = np.hstack((pred_array, new_array))
		# Create Response Variable Array
		resp_array = None
		if mode==TRAINING: # Don't need to do it if not training
			for hndl_Word in self._resp_words:
				# Add History to Array
				new_array = self.get_values_by_col_filtered(word_key(hndl_Word), filter_, values_only=True).reshape(-1,1)
				if resp_array is None:
					resp_array = new_array
				else:
					resp_array = np.hstack((resp_array, new_array))		
			if bootstrap: #ATM, nothing about this is bootstrapped
				len_ = len(pred_array)
				n = len_*BOOTSTRAP_MULTIPLIER
				smp = np.floor(np.random.rand(n)*len_).astype(int)
				pred_array = pred_array[smp]
				resp_array = resp_array[smp]
		return (pred_array, resp_array)

	def save_predictions(self, hndl_Model, hndl_Word):
		if hndl_Word.prediction_requires_raw_data():
			filter_ = self.get_model_filter(mode=PREDICTION_DEPENDENT)
			raw_key = raw_word_key(hndl_Word)
			raw_data = np.array(self.col_array[raw_key][filter_]).reshape(-1)
			raw_predictions = hndl_Model.model.predict(self.get_word_arrays(mode=PREDICTION_DEPENDENT)[0])
		else:
			filter_ = self.get_model_filter(mode=PREDICTION_INDEPENDENT)
			raw_data = None
			raw_predictions = hndl_Model.model.predict(self.get_word_arrays(mode=PREDICTION_INDEPENDENT)[0])
		values = hndl_Word.hndl_Trns.reverse_transform_data(raw_data, raw_predictions)
		dates = self.find_prediction_dates(hndl_Word)
		prd_key = prd_word_key(hndl_Word)
		self.add_column(dates, values, key=prd_key, force=True)

	def get_residual_data(self, hndl_Word):
		raw_key = raw_word_key(hndl_Word)
		prd_key = prd_word_key(hndl_Word)
		prd_ = self.get_series_by_col(prd_key, filter_nulls=False)
		raw_ = self.get_series_by_col(raw_key, filter_nulls=False)
		residuals = prd_ - raw_
		filter_ = ~residuals.isnull()
		smoothed = savitzky_golay(np.array(prd_[filter_]))
		return (smoothed, prd_[filter_], raw_[filter_], residuals[filter_])

	def find_prediction_dates(self, hndl_Word):
		'''
		TODO:
				Use local timeSeries Handle to manage this
					DELETE THIS
				Verify time handles aren't being modified here.
		'''
		if hndl_Word.prediction_requires_raw_data():
			# mode = PREDICTION_DEPENDENT
			time_Arr = [w.hndl_Time for w in self._pred_words]
			time_Arr += [w.hndl_Time_Raw for w in self._resp_words]
		else:
			# mode = PREDICTION_INDEPENDENT
			time_Arr = [w.hndl_Time for w in self._pred_words]
		hndl_Time = reduce(min_time_handle_merge, time_Arr)
		hndl_Word.hndl_Trns.reverse_transform_time(hndl_Time)
		return hndl_Time.get_dates()

	def get_prediction_series(self, hndl_Word):
		prd_key = prd_word_key(hndl_Word)
		return self.get_values_by_col(prd_key, filter_nulls=True)

	def plot_values(self, hndl_Word):
		from util_Testing import plot_data_series
		from handle_TestSeries import EMF_TestSeries_Handle
		raw_key = raw_word_key(hndl_Word)
		prd_key = prd_word_key(hndl_Word)
		raw = EMF_TestSeries_Handle()
		(raw.dates, raw.values) = self.get_values_by_col(raw_key, filter_nulls=True)
		prd = EMF_TestSeries_Handle()
		(prd.dates, prd.values) = self.get_values_by_col(prd_key, filter_nulls=True)
		smooth = EMF_TestSeries_Handle()
		smooth.values = savitzky_golay(np.array(prd.values))
		smooth.dates = prd.dates
		plot_data_series(raw, prd, smooth)

	def response_word_is_set(self):
		return self._resp_words is not None and len(self._resp_words)

	def predictor_words_are_set(self):
		return self._pred_words is not None and len(self._pred_words)

	def get_response_word_types(self):
		return [w.get_model_categorization() for w in self._resp_words]

	def get_predictor_word_types(self):
		return [w.get_model_categorization() for w in self._pred_words]

	# def log_self(self):
	# 	'''
	# 	for testing
	# 	'''
	# 	from util_EMF import dt_epoch_to_str_Y_M_D
	# 	limits = map(dt_epoch_to_str_Y_M_D, self.get_date_limits(mode=TRAINING))
	# 	log.info('WORDSET : training word limits: {0} to {1}'.format(*limits))
	# 	limits = map(dt_epoch_to_str_Y_M_D, self.get_date_limits(mode=PREDICTION_INDEPENDENT))
	# 	log.info('WORDSET : training word limits: {0} to {1}'.format(*limits))

