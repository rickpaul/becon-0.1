# TODO:
#	Clean Up (make play nicer with lib_Model templates, for example)

# EMF 		From...Import
from 	handle_DataSeries		import EMF_DataSeries_Handle
from 	handle_Transformation	import EMF_Transformation_Handle
from 	handle_WordSeries		import EMF_WordSeries_Handle
from 	lib_DBInstructions		import TICKER, retrieve_DataSeries_Filtered, retrieve_DataSeries_All
from 	lib_Runner_Model		import WORD_COUNT_GEOMETRIC_PARAM, MIN_WORD_COUNT
# from 	util_EMF 				import YEARS, QUARTERS, MONTHS, WEEKS, DAYS
from 	util_WordSeries			import generate_Word_Series_name
# EMF 		Import...As
# System 	Import...As
import 	pandas 					as pd
import 	logging 				as log
# System 	From...Import
from 	numpy.random 			import geometric
from 	random 					import choice

class EMF_WordSet_Handle():
	'''
	TODO:
				Make it so data is put in panda DataFrame, so we can just pull out data and know it's time-aligned
	'''
	def __init__(self, dbHandle, template=None):
		self.hndl_DB = dbHandle
		self.predWordCache = {}

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

	def get_response_word_handle_random(self):
		dataHndl = EMF_DataSeries_Handle(self.hndl_DB, ticker=self.respDataTicker)
		trnsPtrn = choice(self.respTrnsPatterns)
		trnsHndl = EMF_Transformation_Handle(trnsPtrn)
		for (key, valList) in self.respTrnsKwargs.iteritems():
			val = choice(valList)
			trnsHndl.set_extra_parameter(key, val)
		self.respWord = EMF_WordSeries_Handle(self.hndl_DB, dataHndl, trnsHndl)
		self.minDate = None
		self.maxDate = None
		return self.respWord

	def get_response_word_handle_current(self):
		return self.respWord

	def get_predictor_word_handles_random_subset(self, numWords=None):
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
			if wordName not in self.predWordCache:
				self.predWordCache[wordName] = wordHndl
			chosen[wordName] = wordHndl
		log.info('WORDSET: Chose {0} words'.format(chosen.keys()))
		self.predWords = chosen
		self.minDate = None
		self.maxDate = None
		return chosen.values()


	def get_word_date_range(self):
		minDate = self.respWord.get_earliest_word_date()
		log.debug('WORDSET: Response Word {0} minDate is {1}'.format(self.respWord, minDate))
		maxDate = self.respWord.get_latest_word_date()
		log.debug('WORDSET: Response Word {0} maxDate is {1}'.format(self.respWord, maxDate))
		for (wordName, word) in self.predWords.iteritems():
			challenger = word.get_earliest_word_date()
			minDate = max(challenger, minDate)
			log.debug('WORDSET: Predictor Word {0} minDate is {1}'.format(word, challenger))
			challenger = word.get_latest_word_date()
			maxDate = min(challenger, maxDate)
			log.debug('WORDSET: Predictor Word {0} maxDate is {1}'.format(word, challenger))
		self.minDate = minDate
		self.maxDate = maxDate
		return (minDate, maxDate)

	# def get_word_date_range(self):
	# 	minDate = self.respWord.get_earliest_word_date()
	# 	maxDate = self.respWord.get_latest_word_date()
	# 	for word in self.predWords.values():
	# 		minDate = max(word.get_earliest_word_date(), minDate)
	# 		maxDate = min(word.get_earliest_word_date(), maxDate)
	# 	self.minDate = minDate
	# 	self.maxDate = maxDate
	# 	return (minDate, maxDate)


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

	# def set_response_word_handle(self, wordHandle):
	# 	'''
	# 	TODO:
	# 				DEPRECATE THIS
	# 	'''
	# 	self.respWord = wordHandle

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
