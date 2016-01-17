# TODO:
#	Remove hndl_DB?
# 	Make play nicer with timeseries i.e. what is point of timeseries


# EMF 		From...Import
from 	handle_TimeSet 			import max_time_handle_merge, min_time_handle_merge
from 	lib_Runner_Model		import BOOTSTRAP_MULTIPLIER
from 	lib_Runner_Model		import TRAINING, PREDICTION, PREDICTION_DEPENDENT
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
		self._hndl_Time = None
		self._sample_weights = None
		self._word_array = None
		self._resp_word = None
		self._pred_words = None
		self._periodicity = None

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

	def resp_word():
		doc = "The Response Word."
		def fget(self):
			return self._resp_word
		def fset(self, value):
			self._resp_word = value
			self.add_word(value)
			# Sloppy
			dates = value.get_raw_dates()
			values = value.get_raw_values()
			newDF = pd.DataFrame({'raw': values.ravel()}, index=dates.ravel())
			self._word_array = pd.concat([self._word_array, newDF], axis=1, ignore_index=False)
		def fdel(self):
			del self._resp_word
		return locals()
	resp_word = property(**resp_word())

	def pred_words():
		doc = "The Predictive Words."
		def fget(self):
			return self._pred_words
		def fset(self, value):
			self._pred_words = value
			for w in self._pred_words:
				self.add_word(w)
		def fdel(self):
			del self._pred_words
		return locals()
	pred_words = property(**pred_words())

	def __word_key(self, hndl_Word):
		return str(hndl_Word)

	def add_word(self, hndl_Word, force=False):
		key = self.__word_key(hndl_Word)
		# Create Word Array, if Necessary
		if self._word_array is None:
			log.info('WORDSET: Creating Word Array.')
			log.info('WORDSET: Adding {0} to Word Array.'.format(key))
			dates = hndl_Word.get_series_dates()
			values = hndl_Word.get_series_values()			
			self._word_array = pd.DataFrame({key: values.ravel()}, index=dates.ravel())
			self._hndl_Time = hndl_Word.hndl_Time
			log.debug('WORDSET: Added {0} points for {1} to Word Array.'.format(len(self._word_array), key))
		# Check for key in Word Array
		elif key in self._word_array and (not force):
			log.info('WORDSET: {0} already in Word Array.'.format(key))
			return
		# Add To Word Array
		else:
			log.info('WORDSET: Adding {0} to Word Array.'.format(key))
			dates = hndl_Word.get_series_dates()
			values = hndl_Word.get_series_values()
			newDF = pd.DataFrame({key: values.ravel()}, index=dates.ravel())
			self._hndl_Time = max_time_handle_merge(hndl_Word.hndl_Time, self._hndl_Time)
			self._word_array = pd.concat([self._word_array, newDF], axis=1, ignore_index=False)
			log.info('WORDSET: Added {0} points for {1} to Word Array.'.format(len(newDF), key))

	def get_model_filter(self, mode=TRAINING):
		if mode == PREDICTION:
			if self.resp_word.prediction_requires_raw_data():
				keys = [self.__word_key(w) for w in self._pred_words]+['raw']
			else:
				keys = [self.__word_key(w) for w in self._pred_words]
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
		# Create Predictor Variable Array
		pred_array = None
		for hndl_Word in self._pred_words:
			new_array = self.get_values_filtered(hndl_Word, filter_)
			if pred_array is None:
				pred_array = new_array
			else:
				pred_array = np.hstack((pred_array, new_array))
		if bootstrap and mode==TRAINING:
			len_ = len(pred_array)
			n = len_*BOOTSTRAP_MULTIPLIER
			smp = np.floor(np.random.rand(n)*len_).astype(int)
			pred_array = pred_array[smp]
			resp_array = resp_array[smp]
		return (pred_array, resp_array)

	def get_prediction_dates(self):
		if self.resp_word.prediction_requires_raw_data():
			# mode = TRAINING
			time_Arr = [w.hndl_Time for w in self._pred_words]
			time_Arr += [self._resp_word.hndl_Data.hndl_Time] #So sloppy.
		else:
			# mode = PREDICTION
			time_Arr = [w.hndl_Time for w in self._pred_words]
		hndl_Time = reduce(min_time_handle_merge, time_Arr)
		self.resp_word.hndl_Trns.reverse_transform_time(hndl_Time)
		return hndl_Time.get_dates()

	def get_prediction_values(self, predictions):
		if self.resp_word.prediction_requires_raw_data():
			filter_ = self.get_model_filter(mode=PREDICTION)
			raw_data = np.array(self._word_array['raw'][filter_]).reshape(-1,1)
			return self.resp_word.hndl_Trns.reverse_transform_data(raw_data, predictions)
		else:
			return self.resp_word.hndl_Trns.reverse_transform_data(None, predictions)


	def response_word_is_set(self):
		return self._resp_word is not None

	def predictor_words_are_set(self):
		return self._pred_words is not None and len(self._pred_words)

	def get_response_word_type(self):
		return self._resp_word.get_model_categorization()

	def get_predictor_word_types(self):
		return [w.get_model_categorization() for w in self._pred_words]

	# def log_self(self):
	# 	'''
	# 	for testing
	# 	'''
	# 	from util_EMF import dt_epoch_to_str_Y_M_D
	# 	limits = map(dt_epoch_to_str_Y_M_D, self.get_date_limits(mode=TRAINING))
	# 	log.info('WORDSET : training word limits: {0} to {1}'.format(*limits))
	# 	limits = map(dt_epoch_to_str_Y_M_D, self.get_date_limits(mode=PREDICTION))
	# 	log.info('WORDSET : training word limits: {0} to {1}'.format(*limits))

