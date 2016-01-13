# TODO:
#	Separate into wordset generator and wordset

# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Transformation	import EMF_Transformation_Handle
from 	handle_WordSeries		import EMF_WordSeries_Handle
from 	lib_DBInstructions		import TICKER, retrieve_DataSeries_Filtered, retrieve_DataSeries_All
from 	lib_Runner_Model		import BOOTSTRAP_MULTIPLIER
from 	lib_Runner_Model		import WORD_COUNT_GEOMETRIC_PARAM, MIN_WORD_COUNT
from 	lib_Runner_Model		import TRAINING, PREDICTION
# from 	util_EMF 				import YEARS, QUARTERS, MONTHS, WEEKS, DAYS
from 	util_WordSeries			import generate_Word_Series_name
# EMF 		Import...As
# System 	Import...As
import 	numpy 					as np
import 	logging 				as log
# System 	From...Import
from 	numpy.random 			import geometric
from 	random 					import choice
from 	functools 				import reduce

class EMF_WordSet_Handle():
	'''
	TODO:
				Make it so data is put in panda DataFrame, so we can just pull out data and know it's time-aligned
	'''
	def __init__(self, dbHandle, template=None):
		self.hndl_DB = dbHandle
		self.predWordCache = {}
		self.sampleWeights = None

		self.respWord = None
		self.respDataTicker = None
		self.respTrnsPatterns = None
		self.respTrnsKwargs = {}

		self.predWords = None
		self.predDataTickers = retrieve_DataSeries_All(self.hndl_DB.cursor_(), column=TICKER)
		self.predTrnsPatterns = None
		self.predTrnsKwargs = {}

	def __remove_pred_data_series(self, ticker):
		try: 
			idx = self.predDataTickers.index(ticker)
			del(self.predDataTickers[idx])
		except ValueError:
			pass # Value not found
		except AttributeError:
			pass # self.predDataTickers is None

	def set_resp_data_ticker(self, ticker, responseNotPredict=False):
		self.respDataTicker = ticker
		if responseNotPredict:
			self.__remove_pred_data_series(ticker)

	def set_resp_trns_ptrns(self, trnsPtrns):
		self.respTrnsPatterns = trnsPtrns

	def set_resp_trns_kwargs(self, trnsKwargs):
		self.respTrnsKwargs = trnsKwargs

	def set_pred_trns_ptrns(self, trnsPtrns):
		self.predTrnsPatterns = trnsPtrns

	def set_pred_trns_kwargs(self, trnsKwargs):
		self.predTrnsKwargs = trnsKwargs

	def clear_resp_word_handle(self):
		self.respWord = None

	def clear_pred_word_handles(self):
		self.predWords = None

	def set_response_word_handle(self, wordHandle):
		self.respWord = wordHandle

	def select_response_word_handle_random(self):
		dataHndl = EMF_DataSeries_Handle(self.hndl_DB, ticker=self.respDataTicker)
		trnsPtrn = choice(self.respTrnsPatterns)
		trnsHndl = EMF_Transformation_Handle(trnsPtrn)
		for (key, valList) in self.respTrnsKwargs.iteritems():
			val = choice(valList)
			trnsHndl.set_extra_parameter(key, val)
		self.respWord = EMF_WordSeries_Handle(self.hndl_DB, dataHndl, trnsHndl)
		log.info('WORDSET: Chose {0} response word'.format(self.respWord))

	def response_word_is_set(self):
		return self.respWord is not None

	def predictor_words_are_set(self):
		return self.predWords is not None and len(self.predWords)

	def get_response_word_handle(self):
		return self.respWord

	def get_response_word_raw(self):
		'''
		FOR TESTING
		'''
		dataHndl = EMF_DataSeries_Handle(self.hndl_DB, ticker=self.respDataTicker)
		trnsHndl = EMF_Transformation_Handle('None')
		return EMF_WordSeries_Handle(self.hndl_DB, dataHndl, trnsHndl)

	def get_response_word_type(self):
		return self.respWord.get_model_categorization()

	def get_predictor_word_handles(self):
		return self.predWords

	def get_predictor_word_types(self):
		return [w.get_model_categorization() for w in self.predWords]

	def select_predictor_word_handles_random(self, numWords=None):
		if numWords is None:
			numWords = geometric(WORD_COUNT_GEOMETRIC_PARAM) + MIN_WORD_COUNT
		log.info('WORDSET: Choosing {0} words'.format(numWords))
		count = 0
		chosen = {}
		while (len(chosen) < numWords) and (count < numWords*10):
			count += 1 # Avoid Infinite Loops
			ticker = choice(self.predDataTickers)
			dataHndl = EMF_DataSeries_Handle(self.hndl_DB, ticker=ticker)
			trnsPtrn = choice(self.predTrnsPatterns)
			trnsHndl = EMF_Transformation_Handle(trnsPtrn)
			for (key, valList) in self.predTrnsKwargs.iteritems():
				val = choice(valList)
				trnsHndl.set_extra_parameter(key, val)
			wordName = generate_Word_Series_name(dataHndl, trnsHndl)
			wordHndl = EMF_WordSeries_Handle(self.hndl_DB, dataHndl, trnsHndl)
			# if wordName not in self.predWordCache:
				# self.predWordCache[wordName] = wordHndl
			chosen[wordName] = wordHndl
			log.info('WORDSET: Chose {0} response word'.format(self.respWord)) # TEST: Delete
		log.info('WORDSET: Chose {0} words'.format(chosen.keys()))
		self.predWords = chosen.values()
		self.features = chosen.keys()

	def get_predicted_values(self, predictions):
		rawValues = self.respWord.get_series_values_original(*self.__get_date_limits(mode=PREDICTION))
		return self.respWord.hndl_Trns.reverse_transform_data(rawValues, predictions)

	def get_predicted_dates(self):
		rawValues = self.respWord.get_series_dates_original(*self.__get_date_limits(mode=PREDICTION))
		return self.respWord.hndl_Trns.reverse_transform_time(rawValues)

	def __get_date_limits(self, mode=TRAINING):
		'''
		TODO:
				Just put the stuff in array and run min/max
		'''
		if mode==TRAINING:
			minDate = self.respWord.get_earliest_word_date()
			maxDate = self.respWord.get_latest_word_date()
			array_ = self.predWords
		elif mode==PREDICTION:
			minDate = self.predWords[0].get_earliest_word_date()
			maxDate = self.predWords[0].get_latest_word_date()
			array_ = self.predWords[1:]
		else:
			raise NameError('mode not recognized.')		
		for word in array_:
			challenger = word.get_earliest_word_date()
			minDate = max(challenger, minDate)
			challenger = word.get_latest_word_date()
			maxDate = min(challenger, maxDate)
		return (minDate, maxDate)

	# def get_date_array(self, mode=TRAINING):
	# 	if mode==TRAINING:
	# 		array_ = self.predWords + [self.respWord]
	# 	elif mode==PREDICTION:
	# 		array_ = self.predWords
	# 	else:
	# 		raise NameError('mode not recognized.')
	# 	return reduce(np.intersect1d, tuple(array_))

	def get_word_arrays(self, mode=TRAINING, bootstrap=False):
		(minDate, maxDate) = self.__get_date_limits(mode=mode)
		# Create Response Variable Array
		respVarArray = None
		if mode==TRAINING:
			for varHandle in [self.respWord]: #We may allow multiple resp words
				# Store history locally for later efficiency
				varHandle.save_series_local()
				# Add history to arary
				if respVarArray is None:
					respVarArray = varHandle.get_series_values_filtered(minDate, maxDate)
				else:
					newArray = varHandle.get_series_values_filtered(minDate, maxDate) # sep out for testing
					respVarArray = np.hstack((respVarArray, newArray))
		# Create Predictor Variable Array
		predVarArray = None
		for varHandle in self.predWords:
			if predVarArray is None:
				predVarArray = varHandle.get_series_values_filtered(minDate, maxDate)
			else:
				newArray = varHandle.get_series_values_filtered(minDate, maxDate) # sep out for testing
				predVarArray = np.hstack((predVarArray, newArray))
		if bootstrap and mode==TRAINING:
			len_ = len(predVarArray)
			n = len_*BOOTSTRAP_MULTIPLIER
			smp = np.floor(np.random.rand(n)*len_).astype(int)
			predVarArray = predVarArray[smp]
			respVarArray = respVarArray[smp]
		return (predVarArray, respVarArray)

	def set_predictor_data_criteria(self,	periodicity=None, 
											earliestDate=None, 
											latestDate=None,
											categorical=None,
											ignoreTickers=[]):
		'''
		TODO:
					Relax earliestDate/latestDate requirement (can get info from incomplete data sets)
		'''
		self.predDataTickers = retrieve_DataSeries_Filtered(	self.hndl_DB.cursor_(), 
																column=TICKER,
																minDate=earliestDate, 
																maxDate=latestDate, 
																periodicity=periodicity, 
																categorical=categorical)
		if self.respDataTicker is not None:
			self.__remove_pred_data_series(self.respDataTicker)
		for ticker in ignoreTickers:
			self.__remove_pred_data_series(ticker)


	# def get_predictor_word_handles_complete_set(self):
	# 	raise NotImplementedError

	# def __get_word(self, dataHndl, trnsHndl):
	# 	wordName = generate_Word_Series_name(dataHndl, trnsHndl)
	# 	if wordName in self.predWordCache:
	# 		return self.predWordCache[wordName]
	# 	else:
	# 		wordHandle = EMF_WordSeries_Handle(self.hndl_DB, dataHndl, trnsHndl)
	# 		self.predWordCache[wordName] = wordHandle
	# 		return wordHandle
