# TODO:
#	Change Doc Strings

# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Transformation	import EMF_Transformation_Handle
from 	handle_WordSeries		import EMF_WordSeries_Handle
from 	lib_DBInstructions		import TICKER, retrieve_DataSeries_Filtered, retrieve_DataSeries_All
from 	lib_Runner_Model		import WORD_COUNT_GEOMETRIC_PARAM, MIN_WORD_COUNT
# System 	Import...As
import 	logging 				as log
# System 	From...Import
from 	numpy.random 			import geometric
from 	random 					import choice



class EMF_WordSelector_Handle(object):
	def __init__(self, hndl_DB):
		self.hndl_DB = hndl_DB
		#
		self._resp_data_tickers = []
		self._resp_trns_ptrns = []
		self._resp_trns_kwargs = {}
		#
		self._resp_word = None
		#
		self._pred_data_tickers = None
		self._pred_trns_ptrns = []
		self._pred_trns_kwargs = {}
		#
		self._resp_can_predict = False
		#
		self._pred_data_periodicity = None
		self._pred_data_max_date = None
		self._pred_data_min_date = None
		self._pred_data_is_categorical = None

	def resp_can_predict():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._resp_can_predict
		def fset(self, value):
			if value != self._resp_can_predict:
				self._pred_data_tickers = None
			self._resp_can_predict = value
		return locals()
	resp_can_predict = property(**resp_can_predict())

	def resp_data_tickers():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._resp_data_tickers
		def fset(self, value):
			self._resp_data_tickers = value
		return locals()
	resp_data_tickers = property(**resp_data_tickers())

	def resp_trns_ptrns():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._resp_trns_ptrns
		def fset(self, value):
			self._resp_trns_ptrns = value
		return locals()
	resp_trns_ptrns = property(**resp_trns_ptrns())

	def resp_trns_kwargs():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._resp_trns_kwargs
		def fset(self, value):
			self._resp_trns_kwargs = value
		return locals()
	resp_trns_kwargs = property(**resp_trns_kwargs())

	def pred_trns_kwargs():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._pred_trns_kwargs
		def fset(self, value):
			self._pred_trns_kwargs = value
		return locals()
	pred_trns_kwargs = property(**pred_trns_kwargs())

	def pred_trns_ptrns():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._pred_trns_ptrns
		def fset(self, value):
			self._pred_trns_ptrns = value
		return locals()
	pred_trns_ptrns = property(**pred_trns_ptrns())

	def pred_data_periodicity():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._pred_data_periodicity
		def fset(self, value):
			if value != self._pred_data_periodicity:
				self._pred_data_tickers = None
			self._pred_data_periodicity = value
		def fdel(self):
			self._pred_data_periodicity = None
		return locals()
	pred_data_periodicity = property(**pred_data_periodicity())

	def pred_data_min_date():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._pred_data_min_date
		def fset(self, value):
			if value != self._pred_data_min_date:
				self._pred_data_tickers = None
			self._pred_data_min_date = value
		def fdel(self):
			self._pred_data_min_date = None
		return locals()
	pred_data_min_date = property(**pred_data_min_date())

	def pred_data_max_date():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._pred_data_max_date
		def fset(self, value):
			if value != self._pred_data_max_date:
				self._pred_data_tickers = None
			self._pred_data_max_date = value
		def fdel(self):
			self._pred_data_max_date = None
		return locals()
	pred_data_max_date = property(**pred_data_max_date())

	def pred_data_is_categorical():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._pred_data_is_categorical
		def fset(self, value):
			if value != self._pred_data_is_categorical:
				self._pred_data_tickers = None
			self._pred_data_is_categorical = value
		def fdel(self):
			self._pred_data_is_categorical = None
		return locals()
	pred_data_is_categorical = property(**pred_data_is_categorical())

	def pred_words():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._pred_words
		def fdel(self):
			self._pred_words = None
		return locals()
	pred_words = property(**pred_words())

	def resp_word():
		doc = 'Response Word Transformation Patterns'
		def fget(self):
			return self._resp_word
		def fdel(self):
			self._resp_word = None
		return locals()
	resp_word = property(**resp_word())

	def __add_pred_data_tickers(self):
		self._pred_data_tickers = retrieve_DataSeries_Filtered(	self.hndl_DB.cursor, 
																column=TICKER,
																minDate=self._pred_data_min_date, 
																maxDate=self._pred_data_max_date, 
																periodicity=self._pred_data_periodicity, 
																categorical=self._pred_data_is_categorical)
		if not self.resp_can_predict:
			for t in self.resp_data_tickers:
				self.__remove_pred_data_tickers(t)

	def __remove_pred_data_tickers(self, ticker):
		try: 
			idx = self._pred_data_tickers.index(ticker)
			del(self._pred_data_tickers[idx])
		except ValueError:
			pass # Value not found

	def select_resp_word_random(self):
		hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, ticker=choice(self.resp_data_tickers))
		hndl_Trns = EMF_Transformation_Handle(choice(self.resp_trns_ptrns))
		for (key, valList) in self.resp_trns_kwargs.iteritems():
			val = choice(valList)
			hndl_Trns.set_extra_parameter(key, val)
		self._resp_word = EMF_WordSeries_Handle(self.hndl_DB, hndl_Data, hndl_Trns)
		log.info('WORDSELECT: Response Word: Chose {0}.'.format(self._resp_word))

	def select_pred_words_random(self, numWords=None):
		assert self._resp_word is not None
		# Add Predictive Words
		if self._pred_data_tickers is None:
			self.__add_pred_data_tickers()
		# Select How Many Words
		if numWords is None:
			numWords = geometric(WORD_COUNT_GEOMETRIC_PARAM) + MIN_WORD_COUNT
		log.info('WORDSELECT: Predictive Words: Choosing {0} words'.format(numWords))
		# Select Words
		count = 0
		chosen = {}
		min_date = self._resp_word.min_date
		max_date = self._resp_word.max_date
		while (len(chosen) < numWords) and (count < numWords*10):
			count += 1 # Avoid Infinite Loops
			ticker = choice(self._pred_data_tickers)
			hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, ticker=choice(self._pred_data_tickers))
			hndl_Trns = EMF_Transformation_Handle(choice(self._pred_trns_ptrns))
			for (key, valList) in self._pred_trns_kwargs.iteritems():
				val = choice(valList)
				hndl_Trns.set_extra_parameter(key, val)
			hndl_Word = EMF_WordSeries_Handle(self.hndl_DB, hndl_Data, hndl_Trns)
			min_challenger = hndl_Word.min_date
			if min_challenger >= max_date:
				continue
			max_challenger = hndl_Word.max_date
			if max_challenger <= min_date:
				continue
			min_date = max(min_date, min_challenger)
			max_date = min(max_date, max_challenger)
			wordName = str(hndl_Word)
			chosen[wordName] = hndl_Word
			log.info('WORDSELECT: Predictive Words: Chose {0}'.format(wordName)) # TEST: Delete
		log.info('WORDSELECT:Predictive Words: Chose {0}'.format(chosen.keys()))
		self._pred_words = chosen.values()

