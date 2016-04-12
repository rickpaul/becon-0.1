# TODO:
#	Change Doc Strings
# 	make resp_word_names one time calculation
# 	make resp_word_ids and pred_word_ids one time calculation
# 		for use in save_data_stats

# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Transformation	import EMF_Transformation_Handle
from 	handle_WordSeries		import EMF_WordSeries_Handle
from 	lib_DBInstructions		import TICKER, retrieve_DataSeries_Filtered, retrieve_DataSeries_All
from 	lib_DBInstructions		import insertStat_DataStatsTable, retrieveStats_DataStatsTable
from 	lib_DBInstructions		import insertStat_WordStatsTable, retrieveStats_WordStatsTable
from 	lib_DBInstructions		import retrieve_DataSeriesTicker, retrieve_DataSeriesID, retrieveAllStats_DataStatsTable
from 	lib_Runner_Model		import PRED_COUNT_GEOMETRIC_PARAM, PRED_COUNT_FLOOR
from 	lib_WordSelector		import SHUFFLED_KEYS, COMBINED_KEYS
from 	util_Stats				import simplify_data_stats_db, simplify_word_stats_db
from 	util_Stats				import weighted_choice
# System 	Import...As
import 	logging 				as log
import 	numpy	 				as np
import 	pandas	 				as pd
# System 	From...Import
from 	numpy.random 			import geometric
from 	random 					import choice, shuffle

class EMF_WordSelector_Handle(object):
	def __init__(self, hndl_DB):
		self.hndl_DB = hndl_DB
		#
		self._resp_data_tickers = None
		self._resp_data_ids = None
		self._resp_trns_ptrns = []
		self._resp_trns_kwargs = {}
		#
		self._resp_words = None
		self._resp_word_ids = None
		self._pred_words = None
		#
		self._pred_data_tickers = None
		self._pred_data_ids = None
		self._pred_data_eff_array = None
		self._pred_trns_ptrns = []
		self._pred_trns_kwargs = {}
		#
		self._resp_can_predict = False
		#
		self._pred_data_periodicity = None
		self._pred_data_max_date = None
		self._pred_data_min_date = None
		self._pred_data_is_categorical = None
		#

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

	def resp_data_tickers():
		doc = 'Response Data Ticker'
		def fget(self):
			return self._resp_data_tickers
		def fset(self, value):
			self._resp_data_tickers = value
			self._resp_data_ids = [retrieve_DataSeriesID(self.hndl_DB.conn, self.hndl_DB.cursor, ticker=t) for t in self._resp_data_tickers]
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
				self._pred_data_ids = None
			self._pred_data_periodicity = value
		def fdel(self):
			self._pred_data_periodicity = None
		return locals()
	pred_data_periodicity = property(**pred_data_periodicity())

	def pred_data_min_date():
		doc = ''
		def fget(self):
			return self._pred_data_min_date
		def fset(self, value):
			if value != self._pred_data_min_date:
				self._pred_data_tickers = None
				self._pred_data_ids = None
			self._pred_data_min_date = value
		def fdel(self):
			self._pred_data_min_date = None
		return locals()
	pred_data_min_date = property(**pred_data_min_date())

	def pred_data_max_date():
		doc = ''
		def fget(self):
			return self._pred_data_max_date
		def fset(self, value):
			if value != self._pred_data_max_date:
				self._pred_data_tickers = None
				self._pred_data_ids = None
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
				self._pred_data_ids = None
			self._pred_data_is_categorical = value
		def fdel(self):
			self._pred_data_is_categorical = None
		return locals()
	pred_data_is_categorical = property(**pred_data_is_categorical())

	def pred_words():
		doc = 'Predictive Word Array'
		def fget(self):
			return self._pred_words
		def fdel(self):
			log.info('WORDSELECT: Removing Predictive Words')
			self._pred_words = None
		return locals()
	pred_words = property(**pred_words())

	def resp_words():
		doc = 'Response Word Array'
		def fget(self):
			return self._resp_words
		def fdel(self):
			log.info('WORDSELECT: Removing Response Words')
			self._resp_words = None
			self._resp_word_ids = None
		return locals()
	resp_words = property(**resp_words())

	def __add_pred_data_tickers(self):
		'''
		TODO:
					Change how pred_data_ids are stored.
		'''
		self._pred_data_tickers = retrieve_DataSeries_Filtered(	self.hndl_DB.cursor, 
																column=TICKER,
																minDate=self._pred_data_min_date, 
																maxDate=self._pred_data_max_date, 
																periodicity=self._pred_data_periodicity, 
																categorical=self._pred_data_is_categorical)
		self._pred_data_ids = [retrieve_DataSeriesID(self.hndl_DB.conn, self.hndl_DB.cursor, ticker=t) for t in self._pred_data_tickers] # Inefficient way to retrieve this...
		if not self.resp_can_predict:
			for t in self.resp_data_tickers:
				self.__remove_pred_data_ticker(t)

	def __remove_pred_data_ticker(self, ticker):
		try: 
			idx = self._pred_data_tickers.index(ticker)
			del(self._pred_data_tickers[idx])
		except ValueError:
			pass # Value not found

	def __create_random_trns_params_resp(self):
		params = {}
		for (key, valList) in self.resp_trns_kwargs.iteritems():
			params[key] = choice(valList)
		return params
		
	def __create_random_trns_params_pred(self):
		params = {}
		for (key, valList) in self.pred_trns_kwargs.iteritems():
			params[key] = choice(valList)
		return params

	def select_resp_words_random(self):
		trns_pattern = choice(self.resp_trns_ptrns)
		trns_params = self.__create_random_trns_params_resp()
		self._resp_words = []
		self._resp_word_ids = []
		for ticker in self.resp_data_tickers:
			hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, ticker=ticker)
			hndl_Trns = EMF_Transformation_Handle(trns_pattern, trnsKwargs=trns_params)
			hndl_Word = EMF_WordSeries_Handle(self.hndl_DB, hndl_Data, hndl_Trns)
			self._resp_words.append(hndl_Word)
			self._resp_word_ids.append(hndl_Word.wordSeriesID)
		log.info('WORDSELECT: Response Word: Chose {0}.'.format([str(w) for w in self.resp_words]))
		return self.resp_words

	def create_data_sorting_array(self, method=SHUFFLED_KEYS):
		'''
		This whole thing is sloppy.
		Rename function
		Rename data array
		'''
		if self._pred_data_eff_array is not None:
			return
		self.simplify_data_statistics()
		self._pred_data_eff_array = pd.DataFrame(index=self._pred_data_ids)
		keys = []
		for hndl_Word in self._resp_words:
			key_ = 'eff.'+str(hndl_Word)
			keys.append(key_)
			stats = retrieveAllStats_DataStatsTable(self.hndl_DB.cursor, hndl_Word.dataSeriesID) # should be n by 2 (seriesID, effectiveness)
			if stats is None:
				new_vals = pd.DataFrame({key_: []}, index=[])
			else:
				effectiveness = np.array(stats)
				new_vals = pd.DataFrame({key_: effectiveness[:,1]}, index=effectiveness[:,0])
			self._pred_data_eff_array = pd.concat([self._pred_data_eff_array, new_vals], axis=1, ignore_index=False)
		if method==SHUFFLED_KEYS:
			shuffle(keys)
			self._pred_data_eff_array = self._pred_data_eff_array.sort_values(keys, axis=0, ascending=False, na_position='first')
			len_ = len(self._pred_data_eff_array)
		elif method==COMBINED_KEYS:
			self._pred_data_eff_array = self._pred_data_eff_array[keys].sum(axis=1, skipna=False)
			self._pred_data_eff_array = self._pred_data_eff_array.sort_values(keys, axis=0, ascending=False, na_position='first')
		else: 
			raise NameError
		self._pred_data_eff_array['prob'] = xrange(len_,0,-1)
		self._total_prob = (len_)*(len_+1)/2
		for key_ in keys:
			del self._pred_data_eff_array[key_]

	def select_pred_words_effectiveness(self, numWords=None):
		assert self.resp_words is not None
		# Add Predictive Words
		if self._pred_data_tickers is None:
			self.__add_pred_data_tickers()
		self.create_data_sorting_array()
		# Select How Many Words
		if numWords is None:
			numWords = geometric(PRED_COUNT_GEOMETRIC_PARAM) + PRED_COUNT_FLOOR
		# Select Words
		count = 0
		chosen = {}
		resp_word_names = [str(w) for w in self.resp_words]
		min_date = max([w.min_date for w in self.resp_words])
		max_date = min([w.max_date for w in self.resp_words])
		while (len(chosen) < numWords) and (count < numWords*10):
			count += 1 # Avoid Infinite Loops
			# Select Words / Create Data Handle
			id_ = weighted_choice(self._pred_data_eff_array['prob'].iteritems(), self._total_prob)
			ticker = retrieve_DataSeriesTicker(self.hndl_DB.cursor, id_)
			hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, ticker=ticker)
			# Select Words / Create Trans Handle
			hndl_Trns = EMF_Transformation_Handle(choice(self._pred_trns_ptrns))
			# Select Words / Create Trans Handle / Add Parameters to Trans Handle
			hndl_Trns.parameters = self.__create_random_trns_params_pred()
			# Select Words / Create Word Handle
			hndl_Word = EMF_WordSeries_Handle(self.hndl_DB, hndl_Data, hndl_Trns)
			# Select Words / Ensure Word Validity
			# Select Words / Ensure Word Validity / Make sure Word Isn't Response Word
			wordName = str(hndl_Word)
			if wordName in resp_word_names:
				continue
			# Select Words / Ensure Word Validity / Make sure Word Isn't Already Taken
			if wordName in chosen:
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
		log.info('WORDSELECT: Predictive Words: Chose {0}'.format(chosen.keys()))
		self._pred_words = chosen.values()
		return self.pred_words

	def select_pred_words_random(self, numWords=None):
		assert self.resp_words is not None
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
		resp_word_names = [str(w) for w in self.resp_words] # TODO: Can make this a one-time calculation to avoid repitition
		min_date = max([w.min_date for w in self.resp_words])
		max_date = min([w.max_date for w in self.resp_words])
		while (len(chosen) < numWords) and (count < numWords*10):
			count += 1 # Avoid Infinite Loops
			# Select Words / Create Data Handle
			hndl_Data = EMF_DataSeries_Handle(self.hndl_DB, ticker=choice(self._pred_data_tickers))
			# Select Words / Create Trans Handle
			hndl_Trns = EMF_Transformation_Handle(choice(self._pred_trns_ptrns))
			# Select Words / Create Trans Handle / Add Parameters to Trans Handle
			hndl_Trns.parameters = self.__create_random_trns_params_pred()
			# Select Words / Create Word Handle
			hndl_Word = EMF_WordSeries_Handle(self.hndl_DB, hndl_Data, hndl_Trns)
			# Select Words / Ensure Word Validity
			# Select Words / Ensure Word Validity / Make sure Word Isn't Response Word
			wordName = str(hndl_Word)
			if wordName in resp_word_names:
				continue
			# Select Words / Ensure Word Validity / Make sure Word Isn't Already Taken
			if wordName in chosen:
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
		log.info('WORDSELECT: Predictive Words: Chose {0}'.format(chosen.keys()))
		self._pred_words = chosen.values()
		return self.pred_words

	def save_word_statistics(self, scores, hndl_Word):
		respID = hndl_Word.wordSeriesID
		for (hndl_Word, score) in zip(self.pred_words, scores):
			predID = hndl_Word.wordSeriesID
			insertStat_WordStatsTable(self.hndl_DB.conn, self.hndl_DB.cursor, 
									  respID, predID, score)

	def simplify_word_statistics(self):
		'''
		'''
		for respID in self._resp_word_ids:
			for hndl_Word in self.pred_words:
				predID = hndl_Word.wordSeriesID
				simplify_word_stats_db(self.hndl_DB.conn, self.hndl_DB.cursor, respID, predID)

	def save_data_statistics(self, scores, hndl_Word):
		respID = hndl_Word.dataSeriesID
		for (hndl_Word, score) in zip(self.pred_words, scores):
			predID = hndl_Word.dataSeriesID
			insertStat_DataStatsTable(self.hndl_DB.conn, self.hndl_DB.cursor, 
									  respID, predID, score)

	def simplify_data_statistics(self):
		'''
		'''
		for respID in self._resp_data_ids:
			for predID in self._pred_data_ids:
				simplify_data_stats_db(self.hndl_DB.conn, self.hndl_DB.cursor, respID, predID)
