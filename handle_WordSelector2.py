# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Transformation	import EMF_Transformation_Handle
from 	handle_WordSeries		import EMF_WordSeries_Handle
from 	lib_DBInstructions		import TICKER, retrieve_DataSeries_Filtered, retrieve_DataSeries_All
from 	lib_Runner_Model		import PRED_COUNT_GEOMETRIC_PARAM, PRED_COUNT_FLOOR
from 	lib_Runner_Model		import RESP_COUNT_GEOMETRIC_PARAM, RESP_COUNT_FLOOR
# System 	Import...As
import 	logging 				as log
# System 	From...Import
from 	numpy.random 			import geometric
from 	random 					import choice


class EMF_WordSelector_Handle2(object):
	def __init__(self, hndl_DB):
		self.hndl_DB = hndl_DB
		#
		self._resp_data_tickers = []
		self._resp_trns_ptrns = []
		self._resp_trns_kwargs = {}
		#
		self._resp_words = None
		self._pred_words = None
		#
		self._pred_data_tickers = None
		self._pred_trns_ptrns = []
		self._pred_trns_kwargs = {}
		#
		self._resp_data_min_date = None
		self._resp_data_max_date = None
		self._resp_data_periodicity = None
		self._pred_data_min_date = None
		self._pred_data_max_date = None
		self._pred_data_periodicity = None
		self._pred_data_is_categorical = None
		#
		self._resp_can_predict = False

	def resp_can_predict():
		doc = 'Response Data can be Predictor Data'
		def fget(self):
			return self._resp_can_predict
		def fset(self, value):
			if value != self._resp_can_predict:
				self._pred_data_tickers = None
			self._resp_can_predict = value
		return locals()
	resp_can_predict = property(**resp_can_predict())

	def pred_words():
		doc = 'Predictive Word Array'
		def fget(self):
			return self._pred_words
		def fdel(self):
			if self._pred_words is not None:
				log.info('WORDSELECT: Removing Predictive Words')
			self._pred_words = None
		return locals()
	pred_words = property(**pred_words())

	def resp_words():
		doc = 'Response Word Array'
		def fget(self):
			return self._resp_words
		def fdel(self):
			if self._resp_words is not None:
				self._resp_words = Nonelog.info('WORDSELECT: Removing Response Words')
			self._resp_words = None
		return locals()
	resp_words = property(**resp_words())

	def resp_data_tickers():
		doc = 'Response Data Tickers'
		def fget(self):
			return self._resp_data_tickers
		def fset(self, value):
			self._resp_data_tickers = value
		def fdel(self):
			del self.resp_words
			self._resp_data_tickers = None
		return locals()
	resp_data_tickers = property(**resp_data_tickers())

	def resp_trns_ptrns():
		doc = 'Predictive Word Transformation Patterns'
		def fget(self):
			return self._resp_trns_ptrns
		def fset(self, value):
			self._resp_trns_ptrns = value
		return locals()
	resp_trns_ptrns = property(**resp_trns_ptrns())

	def resp_trns_kwargs():
		doc = ''
		def fget(self):
			return self._resp_trns_kwargs
		def fset(self, value):
			self._resp_trns_kwargs = value
		return locals()
	resp_trns_kwargs = property(**resp_trns_kwargs())

	def pred_trns_kwargs():
		doc = ''
		def fget(self):
			return self._pred_trns_kwargs
		def fset(self, value):
			self._pred_trns_kwargs = value
		return locals()
	pred_trns_kwargs = property(**pred_trns_kwargs())

	def pred_trns_ptrns():
		doc = ''
		def fget(self):
			return self._pred_trns_ptrns
		def fset(self, value):
			self._pred_trns_ptrns = value
		return locals()
	pred_trns_ptrns = property(**pred_trns_ptrns())

	def pred_data_periodicity():
		doc = ''
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
		doc = 'Data will be at MOST this early. Opposite of resp_data_min_date'
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
		doc = 'Data will be at MOST this late. Opposite of resp_data_max_date'
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
		'''
		TODO: Rename. What is this?!
		'''
		doc = ''
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

	def resp_data_periodicity():
		doc = ''
		def fget(self):
			return self._resp_data_periodicity
		def fset(self, value):
			if value != self._resp_data_periodicity:
				self._resp_data_tickers = None
			self._resp_data_periodicity = value
		def fdel(self):
			self._resp_data_periodicity = None
		return locals()
	resp_data_periodicity = property(**resp_data_periodicity())

	def resp_data_min_date():
		doc = 'Data will be at least this early. Opposite of pred_data_min_date'
		def fget(self):
			return self._resp_data_min_date
		def fset(self, value):
			if value != self._resp_data_min_date:
				self._resp_data_tickers = None
			self._resp_data_min_date = value
		def fdel(self):
			self._resp_data_min_date = None
		return locals()
	resp_data_min_date = property(**resp_data_min_date())

	def resp_data_max_date():
		doc = 'Data will be at least this late. Opposite of pred_data_max_date'
		def fget(self):
			return self._resp_data_max_date
		def fset(self, value):
			if value != self._resp_data_max_date:
				self._resp_data_tickers = None
			self._resp_data_max_date = value
		def fdel(self):
			self._resp_data_max_date = None
		return locals()
	resp_data_max_date = property(**resp_data_max_date())

	def resp_data_is_categorical():
		'''
		TODO: Rename. What is this?!
		'''
		doc = ''
		def fget(self):
			return self._resp_data_is_categorical
		def fset(self, value):
			if value != self._resp_data_is_categorical:
				self._resp_data_tickers = None
			self._resp_data_is_categorical = value
		def fdel(self):
			self._resp_data_is_categorical = None
		return locals()
	resp_data_is_categorical = property(**resp_data_is_categorical())

	def __create_random_trns_params(self, kwargs_list=None):
		if kwargs_list is None:
			kwargs_list = self.resp_trns_kwargs
		params = {}
		for (key, valList) in kwargs_list.iteritems():
			params[key] = choice(valList)
		return params

	def select_resp_words_random(self, numWords=None):
		# Add Response Words
		if self._pred_data_tickers is None:
			self.__add_pred_data_tickers()
		# Select How Many Words
		if numWords is None:
			numWords = geometric(RESP_COUNT_GEOMETRIC_PARAM) + RESP_COUNT_FLOOR
		log.info('WORDSELECT: Response Words: Choosing {0} words'.format(numWords))
		# Select Words
		count = 0
		chosen = {}
		min_date = self.resp_data_min_date
		if min_date is None: min_ = maxint
		max_date = self.resp_data_max_date
		if max_date is None: max_ = -maxint-1
		while (len(chosen) < numWords) and (count < numWords*10):
			count += 1 # Avoid Infinite Loops
			# Select Words / Create Data Handle
			ticker = choice(self._pred_data_tickers)
			hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, ticker=ticker)
			# Select Words / Create Trans Handle
			hndl_Trns = EMF_Transformation_Handle(choice(self._resp_trns_ptrns))
			# Select Words / Create Trans Handle / Add Parameters to Trans Handle
			hndl_Trns.parameters = self.__create_random_trns_params()
			# Select Words / Create Word Handle
			hndl_Word = EMF_WordSeries_Handle(self.hndl_DB, hndl_Data, hndl_Trns)
			# Select Words / Ensure Word Validity
			# Select Words / Ensure Word Validity / Make sure Word Isn't Response Word
			wordName = str(hndl_Word)
			# Select Words / Ensure Word Validity / Make sure Dates Don't Conflict
			min_challenger = hndl_Word.min_date
			if min_challenger >= max_date:
				continue
			max_challenger = hndl_Word.max_date
			if max_challenger <= min_date:
				continue
			min_date = max(min_date, min_challenger)
			max_date = min(max_date, max_challenger)
			# Select Words / Add Word to Set
			chosen[wordName] = hndl_Word
			log.info('WORDSELECT: Response Words: Chose {0}'.format(wordName)) # TEST: Delete
		log.info('WORDSELECT: Response Words: Chose {0}'.format(chosen.keys()))
		self._resp_words = chosen.values()
		return self.resp_words

	def select_resp_words_all_permutations(self):
		log.info('WORDSELECT: Response Words: Choosing All Data Tickers')
		if self._resp_data_tickers is None:
			self.__add_resp_data_tickers()
		log.info('WORDSELECT: Response Words: Choosing All Transformations')
		trns_list = {}
		for trns in self.resp_trns_ptrns:
			for (k, v_list) in self.resp_trns_kwargs.iteritems():
				for v in v_list:
					hndl_Trns = EMF_Transformation_Handle(trns)
					hndl_Trns.set_extra_parameter(k, v)
					trns_list[str(hndl_Trns)] = hndl_Trns
		trns_list = trns_list.values()
		log.info('WORDSELECT: Response Words: Created {0} Transformations'.format(len(trns_list)))
		self._resp_words = []
		count = 0
		for ticker in self.resp_data_tickers:
			hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, ticker=ticker)
			hndl_Data.save_series_local()			
			for hndl_Trns in trns_list:
				hndl_Word = EMF_WordSeries_Handle(self.hndl_DB, hndl_Data, hndl_Trns)
				self._resp_words.append(hndl_Word)
				count += 1
		log.info('WORDSELECT: Response Words: Created {0} Response Words'.format(count))

	def select_pred_words_all_tickers(self, trns_ptrn=None, trns_kwargs=None, trns_rndm=False):
		self._pred_words = []
		log.info('WORDSELECT: Predictive Words: Choosing All Data Tickers')
		if trns_ptrn is None:
			if trns_rndm:
				ticker = choice(self._pred_data_tickers)
			else:
				trns_ptrn = 'None'
		if self._pred_data_tickers is None:
			self.__add_pred_data_tickers()
		hndl_Trns = EMF_Transformation_Handle(trns_ptrn)
		if trns_kwargs is None:
			trns_kwargs = self.pred_trns_kwargs
		hndl_Trns.parameters = self.__create_random_trns_params(kwargs_list=trns_kwargs)
		log.info('WORDSELECT: Predictive Words: Chose {0} Transformation'.format(hndl_Trns))
		for ticker in self._pred_data_tickers:
			hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, ticker=ticker)
			hndl_Word = EMF_WordSeries_Handle(self.hndl_DB, hndl_Data, hndl_Trns)
			self._pred_words.append(hndl_Word)

	def select_pred_words_random(self, numWords=None):
		assert self._resp_word is not None
		# Add Predictive Words
		if self._pred_data_tickers is None:
			self.__add_pred_data_tickers()
		# Select How Many Words
		if numWords is None:
			numWords = geometric(PRED_COUNT_GEOMETRIC_PARAM) + PRED_COUNT_FLOOR
		log.info('WORDSELECT: Predictive Words: Choosing {0} words'.format(numWords))
		# Select Words
		count = 0
		chosen = {}
		min_date = self.resp_data_min_date
		if min_date is None: min_ = maxint
		max_date = self.resp_data_max_date
		if max_date is None: max_ = -maxint-1
		while (len(chosen) < numWords) and (count < numWords*10):
			count += 1 # Avoid Infinite Loops
			# Select Words / Create Data Handle
			ticker = choice(self._resp_data_tickers)
			hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, ticker=ticker)
			# Select Words / Create Trans Handle
			hndl_Trns = EMF_Transformation_Handle(choice(self._pred_trns_ptrns))
			# Select Words / Create Trans Handle / Add Parameters to Trans Handle		
			hndl_Trns.parameters = self.__create_random_trns_params()
			# Select Words / Create Word Handle
			hndl_Word = EMF_WordSeries_Handle(self.hndl_DB, hndl_Data, hndl_Trns)
			# Select Words / Ensure Word Validity
			# Select Words / Ensure Word Validity / Make sure Word Isn't Response Word
			wordName = str(hndl_Word)
			if wordName == str(self._resp_word):
				continue
			# Select Words / Ensure Word Validity / Make sure Dates Don't Conflict
			min_challenger = hndl_Word.min_date
			if min_challenger >= max_date:
				continue
			max_challenger = hndl_Word.max_date
			if max_challenger <= min_date:
				continue
			min_date = max(min_date, min_challenger)
			max_date = min(max_date, max_challenger)
			# Select Words / Add Word to Set
			chosen[wordName] = hndl_Word
			log.info('WORDSELECT: Predictive Words: Chose {0}'.format(wordName)) # TEST: Delete
		log.info('WORDSELECT:Predictive Words: Chose {0}'.format(chosen.keys()))
		self._pred_words = chosen.values()
		return self.pred_words


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


	def __add_resp_data_tickers(self):
		self._resp_data_tickers = retrieve_DataSeries_Filtered(	self.hndl_DB.cursor, 
																column=TICKER,
																atLeastMinDate=self._resp_data_min_date, 
																atLeastMaxDate=self._resp_data_max_date, 
																periodicity=self._resp_data_periodicity, 
																categorical=self._resp_data_is_categorical)
