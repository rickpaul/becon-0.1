# TODO:
#	Remove hndl_DB?
# 	Make play nicer with timeseries i.e. what is point of timeseries


# EMF 		From...Import
from 	handle_TimeSet 			import max_time_handle_merge, min_time_handle_merge
from 	lib_Runner_Model		import BOOTSTRAP_MULTIPLIER
from 	lib_Runner_Model		import TRAINING, PREDICTION_INDEPENDENT, PREDICTION_DEPENDENT
from 	util_Algorithms 		import savitzky_golay
# EMF 		Import...As
# System 	Import...As
import 	numpy 					as np
import 	logging 				as log
import 	pandas	 				as pd
# System 	From...Import
from 	numpy.random 			import geometric
from 	random 					import choice

class EMF_WordSet_Handle(object):
	def __init__(self, hndl_DB):
		self._hndl_DB = hndl_DB
		# self._hndl_Time = None
		self._sample_weights = None
		self._word_array = None
		self._resp_word = None
		self._pred_words = None
		self._pred_filter = None
		self._raw_filter = None
		self._periodicity = None

	def raw_dates():
		doc = "Raw Dates"
		def fget(self):
			return self._word_array[self.resp_raw_key][self.raw_filter].index
		return locals()
	raw_dates = property(**raw_dates())

	def raw_values():
		doc = "Raw Values"
		def fget(self):
			return self._word_array[self.resp_raw_key][self.raw_filter]
		return locals()
	raw_values = property(**raw_values())

	def raw_filter():
		doc = "The raw_filter property."
		def fget(self):
			# if self._raw_filter is None: # Need to recalculate if index changes...
			self._raw_filter = ~self._word_array[self.resp_raw_key].isnull()
			return self._raw_filter
		def fdel(self):
			self._raw_filter = None
		return locals()
	raw_filter = property(**raw_filter())

	def pred_dates():
		doc = "Prediction Values"
		def fget(self):
			return self._word_array[self.resp_pred_key][self.pred_filter].index
		return locals()
	pred_dates = property(**pred_dates())

	def pred_values():
		doc = "Prediction Values"
		def fget(self):
			return self._word_array[self.resp_pred_key][self.pred_filter]
		return locals()
	pred_values = property(**pred_values())

	def pred_filter():
		doc = "The pred_filter property."
		def fget(self):
			# if self._pred_filter is None: # Need to recalculate if index changes...
			self._pred_filter = ~self._word_array[self.resp_pred_key].isnull()
			return self._pred_filter
		def fdel(self):
			self._pred_filter = None
		return locals()
	pred_filter = property(**pred_filter())

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

	def word_array():
		doc = ""
		def fget(self):
			if self._word_array is None:
				self._word_array = pd.DataFrame()
			return self._word_array
		def fdel(self):
			self._word_array = None
		return locals()
	word_array = property(**word_array())

	def resp_word_key():
		def fget(self):
			return self.__word_key(self._resp_word)
		return locals()
	resp_word_key = property(**resp_word_key())

	def resp_raw_key():
		def fget(self):
			return 'raw.'+ self.resp_word_key
		return locals()
	resp_raw_key = property(**resp_raw_key())

	def resp_pred_key():
		def fget(self):
			return 'pred.'+ self.resp_word_key
		return locals()
	resp_pred_key = property(**resp_pred_key())

	def resp_word():
		doc = "The Response Word."
		def fget(self):
			return self._resp_word
		def fset(self, hndl_Word):
			self._resp_word = hndl_Word
			# Add Raw Values
			dates = hndl_Word.get_raw_dates()
			values = hndl_Word.get_raw_values()
			self.__add_word(self.resp_raw_key, dates, values, force=True)
			# Add Transformed Values
			dates = hndl_Word.get_series_dates()
			values = hndl_Word.get_series_values()
			self.__add_word(self.resp_word_key, dates, values, force=True)
		def fdel(self):
			log.info('WORDSET: Removing Response Word')
			del self._resp_word
			del self.pred_filter
			del self.raw_filter
			try:
				del self.word_array[self.resp_pred_key]
			except KeyError:
				log.warning('WORDSET: Unable to delete predictions from word array')
			try:
				del self.word_array[self.resp_raw_key]
			except KeyError:
				log.warning('WORDSET: Unable to delete raw values from word array')
		return locals()
	resp_word = property(**resp_word())

	def pred_words():
		doc = "The Predictive Words."
		def fget(self):
			return self._pred_words
		def fset(self, value):
			self._pred_words = value
			for hndl_Word in self._pred_words:
				dates = hndl_Word.get_series_dates()
				values = hndl_Word.get_series_values()
				key = self.__word_key(hndl_Word)
				self.__add_word(key, dates, values, force=False)
		def fdel(self):
			log.info('WORDSET: Removing Predictive Words')
			del self._pred_words
			try:
				del self.word_array[self.resp_pred_key]
				log.info('WORDSET: Removing Response Prediction Values')
			except KeyError:
				log.warning('WORDSET: Unable to delete predicted values from word array')
		return locals()
	pred_words = property(**pred_words())

	def __word_key(self, hndl_Word):
		return str(hndl_Word)

	def __add_word(self, key, dates, values, force=False):
		if key in self.word_array:
			log.info('WORDSET: {0} already in Word Array.'.format(key))
			if not force:
				return
			else:
				newDF = pd.DataFrame({key:values.ravel()}, index=dates.ravel())
				self._word_array = pd.concat([self._word_array, newDF], axis=1, ignore_index=True)
				log.debug('WORDSET: Added {0} points overwriting {1} in Word Array.'.format(len(self._word_array), key))
		else:
				newDF = pd.DataFrame({key:values.ravel()}, index=dates.ravel())
				self._word_array = pd.concat([self._word_array, newDF], axis=1, ignore_index=False)
				log.debug('WORDSET: Added {0} points for {1} to Word Array.'.format(len(self._word_array), key))
				# self._hndl_Time = max_time_handle_merge(hndl_Word.hndl_Time, self._hndl_Time) # WARNING! Doesn't work if we truncate an end. Forcing messes w it.

	def get_model_filter(self, mode=TRAINING):
		if mode == PREDICTION_INDEPENDENT:
			keys = [self.__word_key(w) for w in self._pred_words]
		elif mode == PREDICTION_DEPENDENT:
			keys = [self.__word_key(w) for w in self._pred_words]+[self.resp_raw_key]
		elif mode == TRAINING:
			keys = [self.__word_key(w) for w in self._pred_words+[self._resp_word]] 
		else:
			raise NameError
		and_ = lambda c1, c2: c1 & c2
		return reduce(and_, [~self._word_array[key].isnull() for key in keys])
		
	def get_values_filtered(self, hndl_Word, filter_):
		key = self.__word_key(hndl_Word)
		return np.array(self._word_array[key][filter_]).reshape(-1,1)

	def get_word_arrays(self, mode=TRAINING, bootstrap=False):
		filter_ = self.get_model_filter(mode=mode)
		# Create Predictor Variable Array
		pred_array = None
		for hndl_Word in self._pred_words:
			new_array = self.get_values_filtered(hndl_Word, filter_)
			if pred_array is None:
				pred_array = new_array
			else:
				pred_array = np.hstack((pred_array, new_array))
		# Create Response Variable Array
		resp_array = None
		if mode==TRAINING: # Don't need to do it if not training
			for hndl_Word in [self._resp_word]: #We may allow multiple resp words
				# Add history to arary
				new_array = self.get_values_filtered(hndl_Word, filter_)
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

	def save_predictions(self, hndl_Model):
		if self.resp_word.prediction_requires_raw_data():
			filter_ = self.get_model_filter(mode=PREDICTION_DEPENDENT)
			raw_data = np.array(self._word_array[self.resp_raw_key][filter_]).reshape(-1)
			raw_predictions = hndl_Model.model.predict(self.get_word_arrays(mode=PREDICTION_DEPENDENT)[0])
		else:
			filter_ = self.get_model_filter(mode=PREDICTION_INDEPENDENT)
			raw_data = None
			raw_predictions = hndl_Model.model.predict(self.get_word_arrays(mode=PREDICTION_INDEPENDENT)[0])
		values = self.resp_word.hndl_Trns.reverse_transform_data(raw_data, raw_predictions)
		dates = self.find_prediction_dates()
		self.__add_word(self.resp_pred_key, dates, values, force=True)

	def get_residual_data(self):
		pred_ = self.pred_values
		raw_ = self.raw_values
		residuals = pred_ - raw_
		filter_ = ~residuals.isnull()
		smoothed = savitzky_golay(np.array(pred_[filter_])) # We should play around with window size and order
		return (smoothed, pred_[filter_], raw_[filter_], residuals[filter_])

	def find_prediction_dates(self): # DELETE
		if self.resp_word.prediction_requires_raw_data():
			# mode = PREDICTION_DEPENDENT
			time_Arr = [w.hndl_Time for w in self._pred_words]
			time_Arr += [self._resp_word.hndl_Data.hndl_Time] #So sloppy.
		else:
			# mode = PREDICTION_INDEPENDENT
			time_Arr = [w.hndl_Time for w in self._pred_words]
		hndl_Time = reduce(min_time_handle_merge, time_Arr)
		self.resp_word.hndl_Trns.reverse_transform_time(hndl_Time)
		return hndl_Time.get_dates()

	def response_word_is_set(self):
		return self._resp_word is not None

	def predictor_words_are_set(self):
		return self._pred_words is not None and len(self._pred_words)

	def get_response_word_types(self):
		return [w.get_model_categorization() for w in [self._resp_word]]

	def get_predictor_word_types(self):
		return [w.get_model_categorization() for w in self._pred_words]

	def plot_values(self):
		from util_Testing import plot_data_series
		from handle_TestSeries import EMF_TestSeries_Handle
		raw = EMF_TestSeries_Handle()
		raw.values = self.raw_values
		raw.dates = self.raw_dates
		pred = EMF_TestSeries_Handle()
		pred.values = self.pred_values
		pred.dates = self.pred_dates
		smooth = EMF_TestSeries_Handle()
		smooth.values = savitzky_golay(np.array(pred.values), 21, 3)
		smooth.dates = pred.dates
		plot_data_series(raw, pred, smooth)

	# def log_self(self):
	# 	'''
	# 	for testing
	# 	'''
	# 	from util_EMF import dt_epoch_to_str_Y_M_D
	# 	limits = map(dt_epoch_to_str_Y_M_D, self.get_date_limits(mode=TRAINING))
	# 	log.info('WORDSET : training word limits: {0} to {1}'.format(*limits))
	# 	limits = map(dt_epoch_to_str_Y_M_D, self.get_date_limits(mode=PREDICTION_INDEPENDENT))
	# 	log.info('WORDSET : training word limits: {0} to {1}'.format(*limits))

