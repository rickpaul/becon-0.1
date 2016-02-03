# EMF 		From...Import
from 	lib_PCA 				import PREDICTOR, RESPONSE, INDEX
from 	lib_PCA 				import WORD_TYPE
# System 	Import...As
import 	logging 				as log
import 	pandas	 				as pd
# System 	From...Import
from 	sklearn.decomposition 	import PCA

class EMF_PCA_Handle(object):
	def __init__(self):
		self._word_array = None
		self._model_info = {}
		self._max_size = None

	def max_size():
		doc = "The max_size property."
		def fget(self):
			return self._max_size
		def fset(self, value):
			self._max_size = value
		return locals()
	max_size = property(**max_size())

	def __center_word_array(self):
		raise NotImplementedError # This isn't working, because we need to normalize the data to a range or std
		self._center_stats_dates = self._word_array.mean(axis=1)
		self._center_stats_words = self._word_array.mean(axis=0)
		self._word_array = self._word_array.subtract(self._center_stats_dates, axis=0)
		self._word_array = self._word_array.subtract(self._center_stats_words, axis=1)

	def run_PCA(self):
		self.__center_word_array()
		copy_word_array = self._word_array.copy()
		for col_name in copy_word_array:
			if self._model_info[col_name][WORD_TYPE] == RESPONSE:
				copy_word_array[col_name] = 0
				# raise NotImplementedError # How are we dealing with NaNs?
			elif self._model_info[col_name][WORD_TYPE] == PREDICTOR:
				pass
			else:
				raise NameError
		model = PCA(n_components='mle', whiten=True)
		model.fit_transform(self._word_array)
		self._results = model.inverse_transform(copy_word_array)

	def add_word(self, hndl_Word, word_type=PREDICTOR):
		self.__add_word_metadata(hndl_Word)
		self.__add_word_history(hndl_Word)

	def __add_word_metadata(self, hndl_Word):
		pass

	def __add_word_history(self, hndl_Word):
		col_name = self.__column_name(hndl_Word)
		values = hndl_Word.values
		dates = hndl_Word.dates
		newValues = pd.DataFrame({col_name: values.ravel()}, index=dates.ravel())
		self._word_array = pd.concat([self._word_array, newValues], axis=1, ignore_index=False)

	def __column_name(self, hndl_Word):
		dict_ = {
			'category' : hndl_Word.category,
			'subcategory' : hndl_Word.subcategory,
			'category_meaning' : hndl_Word.category_meaning,
			'data_ticker' : hndl_Word.data_ticker,
			'transformation' : hndl_Word.trns_code
		}
		str_ = '{category}:{subcategory}:{category_meaning}|{data_ticker}|{transformation}'
		return str_.format(**dict_)

	def create_index(self):
		pass

	def plot_words(self):
		pass
